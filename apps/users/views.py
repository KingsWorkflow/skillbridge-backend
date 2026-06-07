from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required

# Template Views
def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'users/login.html')

def signup_view(request):
    return render(request, 'users/signup.html')

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html', {
        'recommended_careers': [],
        'upcoming_sessions': [],
    })

def logout_view(request):
    logout(request)
    return redirect('home')