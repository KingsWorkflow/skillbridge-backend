from django.contrib import admin
from .models import Project, Certification


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'user__username')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'issuing_organization', 'issue_date')
    search_fields = ('name', 'user__username')