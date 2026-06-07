from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('certifications/', views.certification_list, name='certification_list'),
    path('certifications/create/', views.certification_create, name='certification_create'),
]