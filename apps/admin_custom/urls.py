from django.urls import path
from django.contrib import admin
from .views import analytics_dashboard, bulk_verify_view

urlpatterns = [
    path('analytics/', admin.site.admin_view(analytics_dashboard), name='analytics_dashboard'),
    path('bulk-verify/', admin.site.admin_view(bulk_verify_view), name='bulk_verify'),
]
