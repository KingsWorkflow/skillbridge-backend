import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerificationOTP


def send_otp_email(user):
    otp_code = f"{random.randint(0, 999999):06d}"
    expires_at = timezone.now() + timedelta(minutes=10)

    EmailVerificationOTP.objects.filter(user=user, is_used=False).update(is_used=True)
    EmailVerificationOTP.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)

    subject = "Verify your SkillBridge Nepal account"
    message = (
        f"Hi {user.username},\n\n"
        f"Your verification code is: {otp_code}\n\n"
        "This code will expire in 10 minutes.\n\n"
        "If you did not create an account, please ignore this email.\n\n"
        "Best regards,\nSkillBridge Nepal Team"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    return otp_code


def verify_otp_for_user(user, otp_code):
    otp = (
        EmailVerificationOTP.objects.filter(user=user, is_used=False, otp_code=otp_code)
        .order_by("-created_at")
        .first()
    )
    if not otp:
        return False, "Invalid verification code."
    if otp.expires_at < timezone.now():
        return False, "Verification code has expired."
    otp.is_used = True
    otp.save(update_fields=["is_used"])
    user.email_verified = True
    user.is_active = True
    user.save(update_fields=["email_verified", "is_active"])
    return True, "Email verified successfully."
