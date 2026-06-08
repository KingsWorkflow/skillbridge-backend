from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate API requests using JWT from cookies.
    Falls back to session authentication for non-API requests.
    """
    
    def process_request(self, request):
        # Skip if user is already authenticated via session
        if request.user.is_authenticated:
            return None
        
        # Only process API requests
        if not request.path.startswith('/api/'):
            return None
        
        # Get token from cookie
        access_token = request.COOKIES.get(settings.JWT_COOKIE_NAME)
        refresh_token = request.COOKIES.get(settings.JWT_REFRESH_COOKIE_NAME)
        
        if not access_token:
            return None
        
        # Try to authenticate with the access token
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(access_token)
            user = jwt_auth.get_user(validated_token)
            request.user = user
            request.auth = validated_token
        except (InvalidToken, TokenError):
            # Token is invalid or expired, try to refresh
            if refresh_token:
                from rest_framework_simplejwt.tokens import RefreshToken
                try:
                    refresh = RefreshToken(refresh_token)
                    new_access_token = str(refresh.access_token)
                    # Store new access token in request for response
                    request.new_access_token = new_access_token
                    user = jwt_auth.get_user(refresh)
                    request.user = user
                    request.auth = refresh
                except (InvalidToken, TokenError):
                    # Clear invalid cookies
                    request.clear_jwt_cookies = True
        
        return None
