import uuid
from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('password_changed', 'Password Changed'),
        ('exchange_proposal', 'Exchange Proposal Received'),
        ('proposal_accepted', 'Proposal Accepted'),
        ('proposal_rejected', 'Proposal Rejected'),
        ('session_scheduled', 'Session Scheduled'),
        ('session_reminder', 'Session Reminder'),
        ('session_completed', 'Session Completed'),
        ('skill_verified', 'Skill Verified'),
        ('credit_earned', 'Credit Earned'),
        ('credit_spent', 'Credit Spent'),
        ('certificate_uploaded', 'Certificate Uploaded'),
        ('welcome', 'Welcome'),
        ('message', 'Message'),
    ]
    PREFERRED_TYPE_CHOICES = [
        ('exchange_proposal', 'Exchange Proposal'),
        ('proposal_accepted', 'Proposal Accepted'),
        ('proposal_rejected', 'Proposal Rejected'),
        ('session_scheduled', 'Session Scheduled'),
        ('session_reminder', 'Session Reminder'),
        ('credit_update', 'Credit Update'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    preferred_notification = models.CharField(
        max_length=30,
        choices=PREFERRED_TYPE_CHOICES,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200, default='')
    message = models.TextField()
    link_url = models.CharField(max_length=500, blank=True, help_text='URL to navigate to when clicked')
    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} -> {self.recipient.username}"
