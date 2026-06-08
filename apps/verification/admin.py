from django.contrib import admin
from .models import SkillVerification, Certificate, SkillExam, ExamAttempt


@admin.register(SkillVerification)
class SkillVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'current_level', 'verification_votes')
    list_filter = ('current_level',)
    search_fields = ('user__username', 'skill__name')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'status', 'issue_date')
    list_filter = ('status',)
    search_fields = ('user__username', 'skill__name')


@admin.register(SkillExam)
class SkillExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'skill', 'difficulty', 'is_active')
    list_filter = ('difficulty', 'is_active')


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score', 'passed')
    list_filter = ('passed',)