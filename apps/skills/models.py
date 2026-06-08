from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    popularity_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class TeachableSkill(models.Model):
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='teachable_skills'
    )
    skill = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE,
        related_name='teachers'
    )
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS)
    hourly_commitment = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user} teaches {self.skill}"


class LearnableSkill(models.Model):
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='learnable_skills'
    )
    skill = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE,
        related_name='learners'
    )
    motivation = models.TextField(blank=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user} wants to learn {self.skill}"