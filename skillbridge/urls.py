from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from apps.users import views as user_views

schema_view = get_schema_view(
    openapi.Info(
        title="SkillBridge API",
        default_version='v1',
        description="AI-powered skill exchange platform API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', user_views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('login/', user_views.login_view, name='login_page'),
    path('signup/', user_views.signup_view, name='signup_page'),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)