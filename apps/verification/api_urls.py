from django.urls import path
from . import api_views

app_name = 'verification_api'

urlpatterns = [
    path('status/', api_views.api_verification_status, name='verification_status'),
    path('exams/', api_views.api_exam_list, name='exam_list'),
    path('exams/<int:exam_id>/', api_views.api_exam_detail, name='exam_detail'),
    path('exams/<int:exam_id>/submit/', api_views.api_exam_submit, name='exam_submit'),
    path('community/verify/<int:user_id>/<int:skill_id>/', api_views.api_community_verify, name='community_verify'),
]
