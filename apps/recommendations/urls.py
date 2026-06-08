from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('partners/', views.exchange_partners, name='partners'),
    path('api/partners/', views.api_partners, name='api_partners'),
]