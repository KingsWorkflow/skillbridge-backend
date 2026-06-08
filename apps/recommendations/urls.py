from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('partners/', views.exchange_partners, name='partners'),
    path('api/partners/', views.api_partners, name='api_partners'),
    path('resources/', views.resources, name='resources'),
    path('career/', views.career_recommendations, name='career_recommendations'),
    path('skill-gap/', views.skill_gap, name='skill_gap'),
]