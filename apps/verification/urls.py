from django.urls import path
from . import views

app_name = 'verification'

urlpatterns = [
    path('certificate/upload/', views.upload_certificate, name='upload_certificate'),
    path('community/<int:user_id>/<int:skill_id>/', views.verify_community, name='verify_community'),
    path('exam/<int:skill_id>/start/', views.start_exam, name='start_exam'),
]