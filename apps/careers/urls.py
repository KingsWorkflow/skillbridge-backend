from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('', views.CareerRecommendationView.as_view(), name='career_recommendations'),
    path('refresh/', views.RefreshRecommendationsView.as_view(), name='refresh_recommendations'),
]
