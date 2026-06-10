from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('page/', views.notifications_page, name='notifications_page'),
    path('api/dropdown/', views.notification_dropdown, name='notification_dropdown'),
    path('api/unread-count/', views.unread_count_api, name='unread_count_api'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
]
