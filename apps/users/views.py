from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .forms import CustomUserCreationForm, UserProfileUpdateForm, CustomAuthenticationForm
from .serializers import UserSerializer, LoginSerializer


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('users:dashboard')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, 'Account created successfully!')
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')


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
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user


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


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
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
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeAPIView(APIView):
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


class CreditsAPIView(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'skill_credits': user.skill_credits,
            'beginner_tokens': user.beginner_tokens,
        })