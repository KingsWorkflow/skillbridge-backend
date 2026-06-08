from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    proposer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_proposals'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_proposals'
    )
    offer_skill = models.ForeignKey(
        'skills.TeachableSkill', 
        on_delete=models.CASCADE,
        related_name='proposals_offered'
    )
    request_skill = models.ForeignKey(
        'skills.LearnableSkill', 
        on_delete=models.CASCADE,
        related_name='proposals_requested'
    )
    proposed_hours = models.IntegerField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Proposal from {self.proposer} to {self.receiver}"


class ExchangeSession(models.Model):
    proposal = models.ForeignKey(
        ExchangeProposal, 
        on_delete=models.CASCADE, 
        related_name='sessions'
    )
    scheduled_date = models.DateTimeField()
    duration_hours = models.IntegerField()
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='teaching_sessions'
    )
    learner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='learning_sessions'
    )
    skill_taught = models.ForeignKey(
        'skills.Skill', 
        on_delete=models.CASCADE,
        related_name='sessions_taught'
    )
    completed = models.BooleanField(default=False)
    teacher_rating = models.IntegerField(null=True, blank=True)
    learner_rating = models.IntegerField(null=True, blank=True)
    teacher_feedback = models.TextField(blank=True)
    learner_feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session for {self.proposal}"


class SkillCreditTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('teach_earn', 'Teach Earn'),
        ('learn_spend', 'Learn Spend'),
        ('signup_bonus', 'Signup Bonus'),
        ('referral_bonus', 'Referral Bonus'),
        ('feedback_reward', 'Feedback Reward'),
        ('verification_reward', 'Verification Reward'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    description = models.TextField()
    related_session = models.ForeignKey(
        ExchangeSession, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} credits ({self.transaction_type})"