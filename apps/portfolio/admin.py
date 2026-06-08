from django.contrib import admin
from .models import Project, Certification


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'user__username', 'user__email', 'description')
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    list_select_related = ('user',)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'issuing_organization', 'issue_date', 'verification_url')
    search_fields = ('name', 'user__username', 'user__email', 'issuing_organization')
    list_filter = ('issue_date', 'issuing_organization')
    list_select_related = ('user',)
