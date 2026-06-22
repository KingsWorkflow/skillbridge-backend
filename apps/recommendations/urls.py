from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('partners/', views.exchange_partners, name='partners'),
    path('api/partners/', views.api_partners, name='api_partners'),
    path('resources/', views.resources, name='resources'),
    path('skill-gap/', views.skill_gap, name='skill_gap'),
    path('api/skill-gap/', views.skill_gap_api, name='skill_gap_api'),
    path('search/', views.search, name='search'),
    path('api/search/', views.api_search, name='api_search'),
]