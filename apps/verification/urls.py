from django.urls import path
from . import views

app_name = 'verification'

urlpatterns = [
    path('certificate/', views.certificate_upload, name='certificate_upload'),
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('exam/start/', views.exam_start, name='exam_start'),
    path('exam/submit/', views.exam_submit, name='exam_submit'),
    path('community/<int:user_id>/<int:skill_id>/', views.community_verify, name='community_verify'),
    path('status/<int:user_id>/', views.verification_status, name='verification_status'),
]