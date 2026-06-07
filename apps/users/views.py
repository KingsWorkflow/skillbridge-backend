from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import UserProfile
from .serializers import UserSerializer

# Template Views
def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {
        'recommended_careers': [],
        'upcoming_sessions': [],
    })

@login_required
def portfolio_view(request):
    return render(request, 'portfolio.html', {
        'projects': [],
        'certifications': [],
        'achievements': [],
    })

@login_required
def skill_gap_view(request):
    return render(request, 'skill_gap.html', {
        'priority_goals': [],
        'mentors': [],
    })

@login_required
def skill_exchange_view(request):
    return render(request, 'skill_exchange.html', {
        'listings': [],
    })

@login_required
def career_recommendations_view(request):
    return render(request, 'career_recommendations.html', {
        'career_matches': [],
    })

def resources_view(request):
    return render(request, 'resources.html', {
        'trending_careers': [],
        'internships': [],
    })

def logout_view(request):
    logout(request)
    return redirect('home')

class RegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user