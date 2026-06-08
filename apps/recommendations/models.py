from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class RecommendationCache(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recommendation_cache'
    )
    recommendations = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'created_at')