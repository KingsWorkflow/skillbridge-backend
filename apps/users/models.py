from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class UserProfile(AbstractUser):
    title = models.CharField(max_length=200, blank=True, help_text="Professional title or role, e.g. Full-Stack Developer")
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (0-1 years)'),
        ('intermediate', 'Intermediate (2-4 years)'),
        ('advanced', 'Advanced (5+ years)'),
    ]
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='beginner')
    
    skill_credits = models.IntegerField(default=0)
    beginner_tokens = models.IntegerField(default=5)
    reputation_score = models.FloatField(default=0.0)
    total_hours_taught = models.IntegerField(default=0)
    total_hours_learned = models.IntegerField(default=0)

    linkedin = models.URLField(blank=True, help_text="LinkedIn profile URL")
    github = models.URLField(blank=True, help_text="GitHub profile URL")
    website = models.URLField(blank=True, help_text="Personal portfolio or website URL")
    location = models.CharField(max_length=100, blank=True, help_text="City, Country")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def clean(self):
        """Normalize email to lowercase before saving."""
        if self.email:
            self.email = self.email.lower()
        super().clean()

    def save(self, *args, **kwargs):
        """Normalize email to lowercase before saving."""
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users'


class EmailVerificationOTP(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='email_otps')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP for {self.user.email}"
