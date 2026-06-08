from django.conf import settings
from rest_framework.response import Response


class JWTResponseMixin:
    """
    Mixin to handle JWT cookies in API responses.
    Sets HttpOnly cookies for access and refresh tokens.
    """
    
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        
        # Clear invalid JWT cookies if flagged
        if hasattr(request, 'clear_jwt_cookies') and request.clear_jwt_cookies:
            response.delete_cookie(settings.JWT_COOKIE_NAME)
            response.delete_cookie(settings.JWT_REFRESH_COOKIE_NAME)
            return response
        
        # Set new access token if refreshed
        if hasattr(request, 'new_access_token'):
            response.set_cookie(
                settings.JWT_COOKIE_NAME,
                request.new_access_token,
                max_age=60 * 60,  # 1 hour
                httponly=settings.JWT_COOKIE_HTTP_ONLY,
                secure=settings.JWT_COOKIE_SECURE,
                samesite=settings.JWT_COOKIE_SAMESITE,
            )
        
        return response
