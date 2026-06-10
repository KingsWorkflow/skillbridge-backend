from .models import Notification


def notification_unread_count(request):
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {}
    return {
        'unread_count': Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count(),
    }
