from django.contrib import admin
from .models import Skill, TeachableSkill, LearnableSkill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'popularity_score')
    search_fields = ('name',)


@admin.register(TeachableSkill)
class TeachableSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'proficiency_level', 'hourly_commitment', 'is_active')
    list_filter = ('proficiency_level', 'is_active')


@admin.register(LearnableSkill)
class LearnableSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'urgency')
    list_filter = ('urgency',)