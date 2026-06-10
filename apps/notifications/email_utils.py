from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from .models import Notification


def send_notification_email(notification, request=None):
    if notification.email_sent:
        return
    user = notification.recipient
    if not user.email:
        return

    subject = notification.title
    plain_message = notification.message
    link_url = notification.link_url

    html_message = render_to_string('notifications/email/notification_email.html', {
        'user': user,
        'title': notification.title,
        'message': notification.message,
        'link_url': link_url,
        'notification': notification,
    })

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
        )
        notification.email_sent = True
        notification.save(update_fields=['email_sent'])
    except Exception:
        pass


def create_notification(
    recipient,
    notification_type,
    title,
    message,
    link_url='',
    send_email=True,
):
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        link_url=link_url,
    )
    if send_email:
        send_notification_email(notification)
    return notification


def create_password_changed_notification(user):
    return create_notification(
        recipient=user,
        notification_type='password_changed',
        title='Password Changed Successfully',
        message='Your account password was changed. If you did not initiate this change, please contact support immediately.',
        link_url=reverse('users:profile_edit'),
    )


def create_proposal_notification(receiver, proposer, proposal):
    from apps.exchanges.models import ExchangeProposal
    name = f"@{proposer.username}" if proposer else "A user"
    return create_notification(
        recipient=receiver,
        notification_type='exchange_proposal',
        title='New Skill Exchange Proposal',
        message=f"{name} sent you a skill exchange proposal. They want to learn what you teach.",
        link_url=reverse('exchanges:proposal_list'),
    )


def create_proposal_accepted_notification(proposer, receiver, proposal):
    name = f"@{receiver.username}" if receiver else "A user"
    return create_notification(
        recipient=proposer,
        notification_type='proposal_accepted',
        title='Proposal Accepted!',
        message=f"{name} accepted your skill exchange proposal. Next step: schedule a session.",
        link_url=reverse('exchanges:proposal_list'),
    )


def create_proposal_rejected_notification(proposer, receiver, proposal):
    name = f"@{receiver.username}" if receiver else "A user"
    return create_notification(
        recipient=proposer,
        notification_type='proposal_rejected',
        title='Proposal Update',
        message=f"{name} declined your skill exchange proposal.",
        link_url=reverse('exchanges:proposal_list'),
    )


def create_session_scheduled_notification(proposal, session):
    other = proposal.offer_skill.user if proposal.request_skill.user == session.teacher else session.teacher
    name = f"@{other.username}" if other else "Your partner"
    return [
        create_notification(
            recipient=session.teacher,
            notification_type='session_scheduled',
            title='Session Scheduled',
            message=f"A skill exchange session has been scheduled for {session.scheduled_date}.",
            link_url=reverse('exchanges:proposal_list'),
        ),
        create_notification(
            recipient=session.learner,
            notification_type='session_scheduled',
            title='Session Scheduled',
            message=f"A skill exchange session has been scheduled for {session.scheduled_date}.",
            link_url=reverse('exchanges:proposal_list'),
        ),
    ]


def create_session_reminder_notification(session, hours_before=2):
    return [
        create_notification(
            recipient=session.teacher,
            notification_type='session_reminder',
            title=f'Session Reminder: {hours_before}h left',
            message=f'Your session for {session.skill_taught.name} starts in {hours_before} hours.',
            link_url=reverse('exchanges:proposal_list'),
        ),
        create_notification(
            recipient=session.learner,
            notification_type='session_reminder',
            title=f'Session Reminder: {hours_before}h left',
            message=f'Your session for {session.skill_taught.name} starts in {hours_before} hours.',
            link_url=reverse('exchanges:proposal_list'),
        ),
    ]


def create_session_completed_notification(session):
    return [
        create_notification(
            recipient=session.teacher,
            notification_type='session_completed',
            title='Session Completed',
            message=f'You completed teaching {session.skill_taught.name}. Credits have been added to your account.',
            link_url=reverse('exchanges:proposal_list'),
        ),
        create_notification(
            recipient=session.learner,
            notification_type='session_completed',
            title='Session Completed',
            message=f'You completed learning {session.skill_taught.name}. Credits have been deducted.',
            link_url=reverse('exchanges:proposal_list'),
        ),
    ]


def create_credit_notification(user, amount, transaction_type, description):
    if transaction_type == 'teach_earn':
        return create_notification(
            recipient=user,
            notification_type='credit_earned',
            title='Credits Earned',
            message=f'You earned {amount} credits. {description}',
            link_url=reverse('users:dashboard'),
        )
    else:
        return create_notification(
            recipient=user,
            notification_type='credit_spent',
            title='Credits Spent',
            message=f'{amount} credits have been deducted. {description}',
            link_url=reverse('users:dashboard'),
        )
