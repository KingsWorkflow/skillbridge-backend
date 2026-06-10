from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('teachable/', views.teachable_skills, name='teachable_skills'),
    path('teachable/delete/<int:pk>/', views.delete_teachable_skill, name='teachable_delete'),
    path('teachable/toggle/<int:pk>/', views.toggle_teachable_skill_active, name='teachable_toggle'),
    path('learnable/', views.learnable_skills, name='learnable_skills'),
    path('learnable/delete/<int:pk>/', views.delete_learnable_skill, name='learnable_delete'),
]
