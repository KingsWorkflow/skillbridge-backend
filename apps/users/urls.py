from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
    path('skills/teachable/add/', views.add_teachable_skill, name='add_teachable_skill'),
    path('skills/learnable/add/', views.add_learnable_skill, name='add_learnable_skill'),
    path('skills/teachable/<int:pk>/delete/', views.delete_teachable_skill, name='delete_teachable_skill'),
    path('skills/learnable/<int:pk>/delete/', views.delete_learnable_skill, name='delete_learnable_skill'),
    path('portfolio/projects/add/', views.add_project, name='add_project'),
    path('portfolio/projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('portfolio/certifications/add/', views.add_certification, name='add_certification'),
    path('portfolio/certifications/<int:pk>/delete/', views.delete_certification, name='delete_certification'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# API endpoints
urlpatterns += [
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('api/me/', views.MeAPIView.as_view(), name='api_me'),
    path('api/credits/', views.CreditsAPIView.as_view(), name='api_credits'),
]