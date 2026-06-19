from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny
from .forms import CustomUserCreationForm, UserProfileUpdateForm, CustomAuthenticationForm, OTPVerificationForm, PasswordChangeForm
from apps.skills.forms import TeachableSkillForm, LearnableSkillForm
from .serializers import UserSerializer, LoginSerializer
from .mixins import JWTResponseMixin
from .email_utils import send_otp_email, verify_otp_for_user
from .models import UserProfile
from apps.skills.models import TeachableSkill, LearnableSkill, Skill
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
        user = form.get_user()
        if not user.email_verified:
            messages.error(self.request, 'Please verify your email before logging in. Check your inbox for the OTP code.')
            logout(self.request)
            return redirect('users:verify_email')
        response = super().form_valid(form)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        response.set_cookie(
            settings.JWT_COOKIE_NAME,
            access_token,
            max_age=60 * 60,
            httponly=settings.JWT_COOKIE_HTTP_ONLY,
            secure=settings.JWT_COOKIE_SECURE,
            samesite=settings.JWT_COOKIE_SAMESITE,
        )
        response.set_cookie(
            settings.JWT_REFRESH_COOKIE_NAME,
            refresh_token,
            max_age=60 * 60 * 24,
            httponly=settings.JWT_COOKIE_HTTP_ONLY,
            secure=settings.JWT_COOKIE_SECURE,
            samesite=settings.JWT_COOKIE_SAMESITE,
        )
        return response


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:verify_email')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.email_verified = False
        user.save(update_fields=['is_active', 'email_verified'])
        send_otp_email(user)
        self.request.session['pending_verify_user_id'] = user.id
        messages.success(self.request, 'Account created! Please check your email for the verification code.')
        return redirect('users:verify_email')


class VerifyEmailView(View):
    template_name = 'users/verify_email.html'

    def _get_verify_user(self, request):
        if request.user.is_authenticated and not request.user.is_anonymous:
            return request.user
        user_id = request.session.get('pending_verify_user_id')
        if not user_id:
            return None
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user = self._get_verify_user(request)
        if user and user.email_verified:
            if request.user.is_authenticated:
                return redirect('users:dashboard')
            user.backend = 'apps.users.backends.EmailBackend'
            login(request, user)
            return redirect('users:dashboard')
            user.backend = 'apps.users.backends.EmailBackend'
            login(request, user)
            return redirect('users:dashboard')
        form = OTPVerificationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = self._get_verify_user(request)
        if not user:
            messages.error(request, 'Session expired. Please sign up again.')
            return redirect('users:register')
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            success, message = verify_otp_for_user(user, otp_code)
            if success:
                messages.success(request, message)
                request.session.pop('pending_verify_user_id', None)
                user.backend = 'apps.users.backends.EmailBackend'
                login(request, user)
                return redirect('users:dashboard')
            else:
                messages.error(request, message)
        return render(request, self.template_name, {'form': form})


class ResendOTPView(View):
    def _get_verify_user(self, request):
        if request.user.is_authenticated and not request.user.is_anonymous:
            return request.user
        user_id = request.session.get('pending_verify_user_id')
        if not user_id:
            return None
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request):
        user = self._get_verify_user(request)
        if user and not user.email_verified:
            send_otp_email(user)
            messages.info(request, 'A new verification code has been sent to your email.')
        return redirect('users:verify_email')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@login_required
def dashboard_view(request):
    sent_proposals = request.user.sent_proposals.select_related(
        'offer_skill', 'request_skill', 'receiver'
    ).order_by('-created_at')[:5]
    received_proposals = request.user.received_proposals.select_related(
        'offer_skill', 'request_skill', 'proposer'
    ).order_by('-created_at')[:5]
    
    upcoming_sessions = []
    for session in request.user.learning_sessions.filter(completed=False).select_related('skill_taught').order_by('scheduled_date')[:3]:
        upcoming_sessions.append({
            'skill': session.skill_taught.name,
            'with_user': session.teacher.username,
            'time': session.scheduled_date,
        })
    
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


from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile_edit')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(self.request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachable_skills'] = self.request.user.teachable_skills.select_related('skill').all()
        context['learnable_skills'] = self.request.user.learnable_skills.select_related('skill').all()
        context['form_teachable'] = TeachableSkillForm(user=self.request.user)
        context['form_learnable'] = LearnableSkillForm(user=self.request.user)
        context['password_form'] = PasswordChangeForm()
        return context

    def form_valid(self, form):
        from apps.notifications.email_utils import create_password_changed_notification
        from django.contrib.auth import update_session_auth_hash
        old_password_hash = self.request.user.password
        response = super().form_valid(form)
        new_password_hash = self.object.password
        if old_password_hash != new_password_hash:
            create_password_changed_notification(self.request.user)
            update_session_auth_hash(self.request, self.object)
        return response


@login_required
def public_profile(request, username):
    profile_user = get_object_or_404(UserProfile, username=username)
    
    teachable_skills = TeachableSkill.objects.filter(
        user=profile_user, is_active=True
    ).select_related('skill')
    
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
    if request.method == 'POST':
        form = TeachableSkillForm(request.POST, user=request.user)
        if form.is_valid():
            skill_obj = form.cleaned_data.get('skill')
            proficiency = form.cleaned_data.get('proficiency_level')
            hours = form.cleaned_data.get('hourly_commitment')
            TeachableSkill.objects.get_or_create(
                user=request.user,
                skill=skill_obj,
                defaults={'proficiency_level': proficiency, 'hourly_commitment': hours},
            )
            messages.success(request, 'Skill added successfully!')
            return redirect('users:profile_edit')
    else:
        form = TeachableSkillForm(user=request.user)
    return render(request, 'users/modals/add_skill.html', {'form': form, 'type': 'teachable'})


@login_required
def add_learnable_skill(request):
    if request.method == 'POST':
        form = LearnableSkillForm(request.POST, user=request.user)
        if form.is_valid():
            skill_obj = form.cleaned_data.get('skill')
            motivation = form.cleaned_data.get('motivation', '')
            urgency = form.cleaned_data.get('urgency', 'medium')
            LearnableSkill.objects.get_or_create(
                user=request.user,
                skill=skill_obj,
                defaults={'motivation': motivation, 'urgency': urgency},
            )
            messages.success(request, 'Skill added successfully to your roadmap!')
            return redirect('users:profile_edit')
    else:
        form = LearnableSkillForm(user=request.user)
    return render(request, 'users/modals/add_skill.html', {'form': form, 'type': 'learnable'})


@login_required
def add_project(request):
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
    email_template_name = 'users/password_reset_email_plain.txt'
    html_email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        from apps.notifications.email_utils import create_password_changed_notification
        response = super().form_valid(form)
        create_password_changed_notification(self.user)
        return response


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
            
            response.set_cookie(
                settings.JWT_COOKIE_NAME,
                access_token,
                max_age=60 * 60,
                httponly=settings.JWT_COOKIE_HTTP_ONLY,
                secure=settings.JWT_COOKIE_SECURE,
                samesite=settings.JWT_COOKIE_SAMESITE,
            )
            response.set_cookie(
                settings.JWT_REFRESH_COOKIE_NAME,
                refresh_token,
                max_age=60 * 60 * 24,
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


@login_required
def change_password(request):
    from .forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            from apps.notifications.email_utils import create_password_changed_notification
            create_password_changed_notification(request.user)
            from django.contrib import messages
            messages.success(request, 'Password has been changed successfully.')
            return redirect('users:profile_edit')
    else:
        form = PasswordChangeForm()
    return render(request, 'users/password_change.html', {'form': form})
