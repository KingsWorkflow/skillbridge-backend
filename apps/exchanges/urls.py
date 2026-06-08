from django.urls import path
from . import views

app_name = 'exchanges'

urlpatterns = [
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposals/create/<int:receiver_id>/', views.create_proposal, name='create_proposal'),
    path('proposals/<int:proposal_id>/accept/', views.accept_proposal, name='accept_proposal'),
    path('proposals/<int:proposal_id>/reject/', views.reject_proposal, name='reject_proposal'),
    path('sessions/schedule/<int:proposal_id>/', views.schedule_session, name='schedule_session'),
    path('sessions/<int:session_id>/rate/', views.rate_session, name='rate_session'),
    path('sessions/<int:session_id>/complete/', views.complete_session, name='complete_session'),
]