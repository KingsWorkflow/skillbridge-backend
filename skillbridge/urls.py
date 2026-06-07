from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users import views as user_views

urlpatterns = [
    path('', user_views.home_view, name='home'),
    path('admin/', admin.site.urls),
    
    # API Endpoints - Users (JWT Authentication)
    path('api/', include('apps.users.api_urls')),
    
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
    
    # Frontend Pages - Portfolio
    path('portfolio/', include('apps.portfolio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)