from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ExamAttempt, Certificate, SkillVerification
from apps.skills.models import Skill


@receiver(post_save, sender=ExamAttempt)
def auto_generate_certificate(sender, instance, created, **kwargs):
    if not instance.passed:
        return

    certificate, cert_created = Certificate.objects.get_or_create(
        user=instance.user,
        skill=instance.exam.skill,
        defaults={
            'issuing_organization': 'SkillBridge Nepal',
            'issue_date': timezone.now().date(),
            'status': 'approved',
        }
    )

    verification, v_created = SkillVerification.objects.get_or_create(
        user=instance.user,
        skill=instance.exam.skill,
        defaults={
            'current_level': 3,
            'platform_tested_at': timezone.now(),
        }
    )
    if not v_created and verification.current_level < 3:
        verification.current_level = 3
        verification.platform_tested_at = timezone.now()
        verification.save()
