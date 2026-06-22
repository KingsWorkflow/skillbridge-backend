from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('mission/', views.mission_view, name='mission'),
    path('our-story/', views.our_story_view, name='our_story'),
    path('success-stories/', views.success_stories_view, name='success_stories'),
    path('legal/', views.legal_view, name='legal'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
]
