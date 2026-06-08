from django.contrib import admin, messages
from .models import Skill, TeachableSkill, LearnableSkill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'popularity_score')
    search_fields = ('name', 'category')
    list_filter = ('category',)


@admin.register(TeachableSkill)
class TeachableSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'proficiency_level', 'hourly_commitment', 'is_active', 'created_at')
    list_filter = ('proficiency_level', 'is_active', 'created_at', 'skill__category')
    search_fields = ('user__username', 'user__email', 'skill__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_select_related = ('user', 'skill')
    actions = ['deactivate_skills', 'activate_skills']

    def deactivate_skills(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Deactivated {updated} skills.', messages.SUCCESS)
    deactivate_skills.short_description = 'Deactivate selected skills'

    def activate_skills(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Activated {updated} skills.', messages.SUCCESS)
    activate_skills.short_description = 'Activate selected skills'


@admin.register(LearnableSkill)
class LearnableSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'urgency', 'created_at')
    list_filter = ('urgency', 'created_at', 'skill__category')
    search_fields = ('user__username', 'user__email', 'skill__name', 'motivation')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_select_related = ('user', 'skill')
