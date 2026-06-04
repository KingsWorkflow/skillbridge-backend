from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = ('username', 'email', 'skill_credits', 'beginner_tokens', 'reputation_score')
    fieldsets = UserAdmin.fieldsets + (
        ('Skill Exchange Info', {'fields': ('phone', 'bio', 'experience_level', 'skill_credits', 'beginner_tokens', 'reputation_score', 'total_hours_taught', 'total_hours_learned')}),
    )

admin.site.register(UserProfile, CustomUserAdmin)