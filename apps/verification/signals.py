from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ExamAttempt, Certificate
from apps.skills.models import Skill


@receiver(post_save, sender=ExamAttempt)
def auto_generate_certificate(sender, instance, created, **kwargs):
    if not instance.passed:
        return

    existing = Certificate.objects.filter(
        user=instance.user,
        skill=instance.exam.skill,
        status='approved',
    ).exists()
    if existing:
        return

    Certificate.objects.create(
        user=instance.user,
        skill=instance.exam.skill,
        issuing_organization='SkillBridge Nepal',
        issue_date=timezone.now().date(),
        status='approved',
    )
