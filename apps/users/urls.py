from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', views.UserProfileView.as_view(), name='user_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('skill-gap/', views.skill_gap_view, name='skill_gap'),
    path('skill-exchange/', views.skill_exchange_view, name='skill_exchange'),
    path('career-recommendations/', views.career_recommendations_view, name='career_recommendations'),
    path('resources/', views.resources_view, name='resources'),
]