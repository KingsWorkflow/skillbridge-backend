from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View
from django.http import HttpResponseRedirect
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny
from .forms import CustomUserCreationForm, UserProfileUpdateForm, CustomAuthenticationForm
from .serializers import UserSerializer, LoginSerializer
from .mixins import JWTResponseMixin
from apps.skills.models import TeachableSkill, LearnableSkill, Skill
from apps.skills.forms import TeachableSkillForm, LearnableSkillForm
from apps.portfolio.models import Project, Certification as PortfolioCertification
from apps.portfolio.forms import ProjectForm, CertificationForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('users:dashboard')

    def form_valid(self, form):
        # Session-based login for Django templates
        response = super().form_valid(form)
        
        # Also set JWT cookies for API access
        user = form.get_user()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        response.set_cookie(
            settings.JWT_COOKIE_NAME,
            access_token,
            max_age=60 * 60,  # 1 hour
            httponly=settings.JWT_COOKIE_HTTP_ONLY,
            secure=settings.JWT_COOKIE_SECURE,
            samesite=settings.JWT_COOKIE_SAMESITE,
        )
        response.set_cookie(
            settings.JWT_REFRESH_COOKIE_NAME,
            refresh_token,
            max_age=60 * 60 * 24,  # 1 day
            httponly=settings.JWT_COOKIE_HTTP_ONLY,
            secure=settings.JWT_COOKIE_SECURE,
            samesite=settings.JWT_COOKIE_SAMESITE,
        )
        
        return response


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=email, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, 'Account created successfully!')
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@login_required
def dashboard_view(request):
    # Get recent proposals (sent and received)
    sent_proposals = request.user.sent_proposals.select_related(
        'offer_skill', 'request_skill', 'receiver'
    ).order_by('-created_at')[:5]
    received_proposals = request.user.received_proposals.select_related(
        'offer_skill', 'request_skill', 'proposer'
    ).order_by('-created_at')[:5]
    
    # Get upcoming sessions
    upcoming_sessions = []
    for session in request.user.learning_sessions.filter(completed=False).select_related('skill_taught').order_by('scheduled_date')[:3]:
        upcoming_sessions.append({
            'skill': session.skill_taught.name,
            'with_user': session.teacher.username,
            'time': session.scheduled_date,
        })
    
    # Mock recommended careers
    recommended_careers = [
        {'title': 'Full-Stack Developer', 'match_type': 'Hot', 'description': 'Build web applications end-to-end'},
        {'title': 'Data Scientist', 'match_type': 'Growing', 'description': 'Extract insights from data'},
    ]
    
    context = {
        'skill_credits': request.user.skill_credits,
        'beginner_tokens': request.user.beginner_tokens,
        'reputation_score': request.user.reputation_score,
        'total_hours_taught': request.user.total_hours_taught,
        'total_hours_learned': request.user.total_hours_learned,
        'recommended_careers': recommended_careers,
        'upcoming_sessions': upcoming_sessions,
        'gap_score': 70,
        'priority_skill': 'System Design',
        'recent_proposals': {
            'sent': sent_proposals,
            'received': received_proposals,
        },
    }
    return render(request, 'users/dashboard.html', context)


class ProfileUpdateView(UpdateView):
    form_class = UserProfileUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile_edit')

    def get_object(self):
        return self.request.user


@login_required
def public_profile(request, username):
    """View any user's public profile."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    profile_user = get_object_or_404(User, username=username)
    
    teachable_skills = TeachableSkill.objects.filter(
        user=profile_user, is_active=True
    ).select_related('skill', 'verification')
    
    learnable_skills = LearnableSkill.objects.filter(
        user=profile_user
    ).select_related('skill')
    
    projects = profile_user.projects.all()
    certifications = profile_user.certifications.all()
    
    is_own_profile = request.user == profile_user
    
    return render(request, 'users/profile_public.html', {
        'profile_user': profile_user,
        'teachable_skills': teachable_skills,
        'learnable_skills': learnable_skills,
        'projects': projects,
        'certifications': certifications,
        'is_own_profile': is_own_profile,
    })


@login_required
def add_teachable_skill(request):
    """Add a teachable skill for the current user."""
    if request.method == 'POST':
        form = TeachableSkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('users:profile_edit')
    else:
        form = TeachableSkillForm()
    
    return render(request, 'users/modals/add_skill.html', {'form': form, 'type': 'teachable'})


@login_required
def add_learnable_skill(request):
    """Add a learnable skill for the current user."""
    if request.method == 'POST':
        form = LearnableSkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('users:profile_edit')
    else:
        form = LearnableSkillForm()
    
    return render(request, 'users/modals/add_skill.html', {'form': form, 'type': 'learnable'})


@login_required
def add_project(request):
    """Add a portfolio project."""
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, 'Project added!')
            return redirect('users:profile_edit')
    else:
        form = ProjectForm()
    
    return render(request, 'users/modals/add_project.html', {'form': form})


@login_required
def add_certification(request):
    """Add a certification."""
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.user = request.user
            cert.save()
            messages.success(request, 'Certification added!')
            return redirect('users:profile_edit')
    else:
        form = CertificationForm()
    
    return render(request, 'users/modals/add_certification.html', {'form': form})


@login_required
def delete_teachable_skill(request, pk):
    skill = get_object_or_404(TeachableSkill, pk=pk, user=request.user)
    skill.delete()
    messages.success(request, 'Skill removed.')
    return redirect('users:profile_edit')


@login_required
def delete_learnable_skill(request, pk):
    skill = get_object_or_404(LearnableSkill, pk=pk, user=request.user)
    skill.delete()
    messages.success(request, 'Skill removed.')
    return redirect('users:profile_edit')


@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    project.delete()
    messages.success(request, 'Project removed.')
    return redirect('users:profile_edit')


@login_required
def delete_certification(request, pk):
    cert = get_object_or_404(PortfolioCertification, pk=pk, user=request.user)
    cert.delete()
    messages.success(request, 'Certification removed.')
    return redirect('users:profile_edit')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


def home_view(request):
    return render(request, 'home.html')


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'experience_level': user.experience_level,
                    'skill_credits': user.skill_credits,
                    'beginner_tokens': user.beginner_tokens,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(JWTResponseMixin, APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            response = Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'experience_level': user.experience_level,
                    'skill_credits': user.skill_credits,
                    'beginner_tokens': user.beginner_tokens,
                },
                'access': access_token,
                'refresh': refresh_token,
            })
            
            # Set JWT cookies
            response.set_cookie(
                settings.JWT_COOKIE_NAME,
                access_token,
                max_age=60 * 60,  # 1 hour
                httponly=settings.JWT_COOKIE_HTTP_ONLY,
                secure=settings.JWT_COOKIE_SECURE,
                samesite=settings.JWT_COOKIE_SAMESITE,
            )
            response.set_cookie(
                settings.JWT_REFRESH_COOKIE_NAME,
                refresh_token,
                max_age=60 * 60 * 24,  # 1 day
                httponly=settings.JWT_COOKIE_HTTP_ONLY,
                secure=settings.JWT_COOKIE_SECURE,
                samesite=settings.JWT_COOKIE_SAMESITE,
            )
            
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeAPIView(JWTResponseMixin, APIView):
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'bio': user.bio,
            'experience_level': user.experience_level,
            'skill_credits': user.skill_credits,
            'beginner_tokens': user.beginner_tokens,
            'reputation_score': user.reputation_score,
            'total_hours_taught': user.total_hours_taught,
            'total_hours_learned': user.total_hours_learned,
        })
    
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreditsAPIView(JWTResponseMixin, APIView):
    def get(self, request):
        user = request.user
        return Response({
            'skill_credits': user.skill_credits,
            'beginner_tokens': user.beginner_tokens,
        })