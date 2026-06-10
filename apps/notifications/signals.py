from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.exchanges.models import ExchangeProposal, ExchangeSession
from apps.verification.models import Certificate
from . import email_utils


User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_notification(sender, instance, created, **kwargs):
    if created:
        email_utils.create_notification(
            recipient=instance,
            notification_type='welcome',
            title='Welcome to SkillBridge Nepal!',
            message='Your account has been registered. Please check your email to verify your account and get started.',
            link_url='/verify-email/',
            send_email=False,
        )


@receiver(post_save, sender=ExchangeProposal)
def proposal_created(sender, instance, created, **kwargs):
    if created and instance.proposer != instance.receiver:
        email_utils.create_proposal_notification(instance.receiver, instance.proposer, instance)


@receiver(post_save, sender=ExchangeProposal)
def proposal_updated(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = ExchangeProposal.objects.filter(pk=instance.pk).first()
    if not old:
        return
    if old.status == 'pending' and instance.status == 'accepted':
        email_utils.create_proposal_accepted_notification(instance.proposer, instance.receiver, instance)
    elif old.status == 'pending' and instance.status == 'rejected':
        email_utils.create_proposal_rejected_notification(instance.proposer, instance.receiver, instance)


@receiver(post_save, sender=ExchangeSession)
def session_created(sender, instance, created, **kwargs):
    if created:
        email_utils.create_session_scheduled_notification(instance.proposal, instance)


@receiver(post_save, sender=ExchangeSession)
def session_completed_signal(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = ExchangeSession.objects.filter(pk=instance.pk).first()
    if not old:
        return
    if not old.completed and instance.completed:
        email_utils.create_session_completed_notification(instance)


@receiver(post_save, sender=Certificate)
def certificate_uploaded(sender, instance, created, **kwargs):
    if created:
        email_utils.create_notification(
            recipient=instance.user,
            notification_type='certificate_uploaded',
            title='Certificate Uploaded',
            message=f'Your certificate for {instance.skill.name} has been submitted for verification.',
            link_url='/verification/certificates/',
        )
