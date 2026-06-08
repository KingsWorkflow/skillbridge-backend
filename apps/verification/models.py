from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SkillVerification(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='verifications'
    )
    skill = models.ForeignKey(
        'skills.Skill', 
        on_delete=models.CASCADE,
        related_name='verifications'
    )
    current_level = models.IntegerField(default=0)
    self_declared_at = models.DateTimeField(auto_now_add=True)
    community_verified_at = models.DateTimeField(null=True, blank=True)
    certificate_verified_at = models.DateTimeField(null=True, blank=True)
    platform_tested_at = models.DateTimeField(null=True, blank=True)
    expert_achieved_at = models.DateTimeField(null=True, blank=True)
    verification_votes = models.IntegerField(default=0)
    total_teaching_hours = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user} - {self.skill} (Level {self.current_level})"


class Certificate(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='certificates_uploaded'
    )
    skill = models.ForeignKey(
        'skills.Skill', 
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    certificate_file = models.FileField(upload_to='certificates/')
    issuing_organization = models.CharField(max_length=200)
    certificate_id = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='certificates_verified'
    )
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Certificate for {self.skill} by {self.user}"


class SkillExam(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    skill = models.ForeignKey(
        'skills.Skill', 
        on_delete=models.CASCADE,
        related_name='exams'
    )
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    title = models.CharField(max_length=200)
    time_limit_minutes = models.IntegerField(default=30)
    passing_score = models.IntegerField(default=70)
    questions = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.skill}"


class ExamAttempt(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='exam_attempts'
    )
    exam = models.ForeignKey(
        'SkillExam', 
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    score = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)
    answers = models.JSONField()
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    can_retake_after = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.exam}"