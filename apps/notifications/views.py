from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from .models import Notification


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()[:50]
    unread_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def notification_dropdown(request):
    notifications = request.user.notifications.all()[:10]
    unread_count = request.user.notifications.filter(is_read=False).count()
    html = render_to_string('notifications/partials/dropdown.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'user': request.user,
    })
    return JsonResponse({'html': html, 'unread_count': unread_count})


@login_required
@require_POST
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    return JsonResponse({'success': True})


@login_required
@require_POST
def mark_all_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'success': True})


@login_required
@require_POST
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    unread_count = request.user.notifications.filter(is_read=False).count()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'unread_count': unread_count})
    messages.success(request, 'Notification deleted successfully.')
    return redirect('notifications:notification_list')


@login_required
def unread_count_api(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'unread_count': count})


@login_required
def notifications_page(request):
    notifications = request.user.notifications.all()
    unread_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'notifications/notification_page.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })
