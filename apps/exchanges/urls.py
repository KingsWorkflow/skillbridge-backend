from django.urls import path
from . import views

app_name = 'exchanges'

urlpatterns = [
    path('', views.exchange_list, name='exchange_list'),
    path('skill-exchange/', views.skill_exchange, name='skill_exchange'),
    path('proposals/create/', views.proposal_create, name='proposal_create'),
    path('sessions/schedule/', views.session_schedule, name='session_schedule'),
]