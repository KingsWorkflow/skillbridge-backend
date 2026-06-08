from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('teachable/', views.teachable_skills, name='teachable'),
    path('learnable/', views.learnable_skills, name='learnable'),
]