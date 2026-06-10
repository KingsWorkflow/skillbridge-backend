from django.db import models
from django.contrib.auth import get_user_model
from apps.skills.models import Skill

User = get_user_model()


class CareerPath(models.Model):
    """Represents a career path with required skills and metadata."""

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill, related_name='career_paths')
    average_salary = models.CharField(max_length=100, blank=True, help_text='e.g., NPR 1,200,000 - 2,500,000 per year')
    growth_outlook = models.CharField(max_length=100, blank=True, help_text='e.g., +25% YoY')
    estimated_hours_per_skill = models.JSONField(default=dict, blank=True, help_text='Map skill_id or skill name -> estimated hours')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Career Path'
        verbose_name_plural = 'Career Paths'

    def __str__(self):
        return self.title
