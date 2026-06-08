from django.contrib import admin, messages
from django.db.models import F
from .models import SkillVerification, Certificate, SkillExam, ExamAttempt


@admin.register(SkillVerification)
class SkillVerificationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'skill',
        'current_level',
        'verification_votes',
        'total_teaching_hours',
        'average_rating',
        'self_declared_at',
    )
    list_filter = ('current_level', 'self_declared_at', 'community_verified_at')
    search_fields = ('user__username', 'user__email', 'skill__name')
    readonly_fields = (
        'self_declared_at',
        'community_verified_at',
        'certificate_verified_at',
        'platform_tested_at',
        'expert_achieved_at',
    )
    list_select_related = ('user', 'skill')
    actions = ['increase_level', 'decrease_level']

    def increase_level(self, request, queryset):
        updated = queryset.update(current_level=F('current_level') + 1)
        self.message_user(request, f'Increased level for {updated} records.', messages.SUCCESS)
    increase_level.short_description = 'Increase verification level (+1)'

    def decrease_level(self, request, queryset):
        updated = queryset.exclude(current_level=0).update(current_level=F('current_level') - 1)
        self.message_user(request, f'Decreased level for {updated} records.', messages.SUCCESS)
    decrease_level.short_description = 'Decrease verification level (-1)'


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'skill',
        'status',
        'issuing_organization',
        'issue_date',
        'verified_at',
    )
    list_filter = ('status', 'issue_date', 'verified_at', 'issuing_organization')
    search_fields = (
        'user__username',
        'user__email',
        'skill__name',
        'issuing_organization',
        'certificate_id',
    )
    readonly_fields = ('verified_at',)
    date_hierarchy = 'issue_date'
    list_select_related = ('user', 'skill', 'verified_by')
    actions = ['approve_certificates', 'reject_certificates']
    list_editable = ('status',)

    def approve_certificates(self, request, queryset):
        from django.utils import timezone
        count = queryset.filter(status='pending').update(
            status='approved',
            verified_at=timezone.now(),
            verified_by=request.user,
        )
        self.message_user(request, f'Approved {count} certificates.', messages.SUCCESS)
    approve_certificates.short_description = 'Approve selected certificates'

    def reject_certificates(self, request, queryset):
        count = queryset.filter(status='pending').update(status='rejected', verified_by=request.user)
        self.message_user(request, f'Rejected {count} certificates.', messages.WARNING)
    reject_certificates.short_description = 'Reject selected certificates'


@admin.register(SkillExam)
class SkillExamAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'skill',
        'difficulty',
        'time_limit_minutes',
        'passing_score',
        'is_active',
        'created_at',
    )
    list_filter = ('difficulty', 'is_active', 'created_at')
    search_fields = ('title', 'skill__name', 'questions')
    readonly_fields = ('created_at',)
    list_select_related = ('skill',)


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'exam',
        'score',
        'passed',
        'started_at',
        'completed_at',
    )
    list_filter = ('passed', 'started_at', 'completed_at', 'exam__difficulty')
    search_fields = ('user__username', 'user__email', 'exam__title')
    readonly_fields = ('started_at', 'completed_at', 'answers')
    list_select_related = ('user', 'exam')
