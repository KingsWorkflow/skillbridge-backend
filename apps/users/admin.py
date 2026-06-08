from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from apps.skills.models import TeachableSkill, LearnableSkill


class TeachableSkillInline(admin.TabularInline):
    model = TeachableSkill
    extra = 0
    fields = ('skill', 'proficiency_level', 'hourly_commitment', 'is_active')
    raw_id_fields = ('skill',)


class LearnableSkillInline(admin.TabularInline):
    model = LearnableSkill
    extra = 0
    fields = ('skill', 'urgency', 'motivation')
    raw_id_fields = ('skill',)


@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    model = UserProfile
    inlines = [TeachableSkillInline, LearnableSkillInline]
    list_display = (
        'username',
        'email',
        'experience_level',
        'skill_credits',
        'reputation_score',
        'is_active',
        'date_joined',
    )
    list_filter = ('experience_level', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'bio')
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined', 'last_login', 'reputation_score')
    actions = ['activate_users', 'deactivate_users', 'recalculate_reputation']

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Activated {updated} users.', messages.SUCCESS)
    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Deactivated {updated} users.', messages.SUCCESS)
    deactivate_users.short_description = 'Deactivate selected users'

    def recalculate_reputation(self, request, queryset):
        for user in queryset:
            sessions = user.teaching_sessions.filter(completed=True)
            ratings = [s.teacher_rating for s in sessions if s.teacher_rating is not None]
            user.reputation_score = sum(ratings) / len(ratings) if ratings else 0.0
            user.save(update_fields=['reputation_score'])
        self.message_user(request, f'Recalculated reputation for {queryset.count()} users.', messages.SUCCESS)
    recalculate_reputation.short_description = 'Recalculate reputation score'
