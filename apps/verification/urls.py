from django.urls import path
from . import views

app_name = 'verification'

urlpatterns = [
    path('community/<int:user_id>/<int:skill_id>/', views.verify_community, name='verify_community'),
    path('exam/<int:skill_id>/start/', views.start_exam, name='start_exam'),
    path('exam/submit/', views.exam_submit, name='exam_submit'),
    path('status/', views.verification_status, name='verification_status'),
    path('certificates/', views.certificate_list, name='certificate_list'),
]
