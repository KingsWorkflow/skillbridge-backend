from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users import views as user_views

urlpatterns = [
    path('', user_views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('admin/', include('apps.admin_custom.urls')),
    
    # API Endpoints - Users (JWT Authentication)
    path('api/', include('apps.users.api_urls')),
    path('api/skills/', include('apps.skills.api_urls')),
    
    # Frontend Pages - Users
    path('', include('apps.users.urls')),
    
    # Frontend Pages - Skills
    path('skills/', include('apps.skills.urls')),
    
    # Frontend Pages - Exchanges
    path('exchanges/', include('apps.exchanges.urls')),
    
    # Frontend Pages - Recommendations
    path('recommendations/', include('apps.recommendations.urls')),
    
    # Frontend Pages - Verification
    path('verification/', include('apps.verification.urls')),
    path('api/verification/', include('apps.verification.api_urls')),
    
    # Frontend Pages - Portfolio
    path('portfolio/', include('apps.portfolio.urls')),
    
    # Frontend Pages - Careers
    path('career/', include('apps.careers.urls')),
    
    # Frontend Pages - Notifications
    path('notifications/', include('apps.notifications.urls')),
    
    # Frontend Pages - Static Content
    path('', include('apps.pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)