from django.apps import AppConfig
from django.contrib import admin
from django.urls import path


class AdminCustomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin_custom'
    label = 'admin_custom'

    def ready(self):
        from apps.admin_custom.views import analytics_dashboard, bulk_verify_view

        original_get_urls = admin.site.get_urls

        def get_urls():
            urls = original_get_urls()
            extra = [
                path('analytics/', admin.site.admin_view(analytics_dashboard), name='analytics_dashboard'),
                path('bulk-verify/', admin.site.admin_view(bulk_verify_view), name='bulk_verify'),
            ]
            return extra + urls

        admin.site.get_urls = get_urls
