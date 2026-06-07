from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('career/', views.career_recommendations, name='career_recommendations'),
    path('skills/', views.skill_recommendations, name='skill_recommendations'),
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('skill-gap/', views.skill_gap, name='skill_gap'),
    path('resources/', views.resources, name='resources'),
]