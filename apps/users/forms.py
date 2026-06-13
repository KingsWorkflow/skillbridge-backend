from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator

User = get_user_model()

NEPALI_PHONE_REGEX = RegexValidator(
    regex=r'^(?:(?:\+977[-]?\d{10,12})|(?:9\d{9}))$',
    message='Enter a valid Nepali phone number (e.g. 9812345678 or +977-9812345678).',
)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'w-full pl-12 pr-12 py-4 bg-surface-container-low border border-on-surface/10 rounded-lg focus:ring-2 focus:ring-secondary/20 focus:border-secondary outline-none transition-all font-body-md text-body-md required', 'autofocus': True, 'type': 'email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'w-full pl-12 pr-12 py-4 bg-surface-container-low border border-on-surface/10 rounded-lg focus:ring-2 focus:ring-secondary/20 focus:border-secondary outline-none transition-all font-body-md text-body-md required'})
    )

    def clean_username(self):
        """Normalize username (email) to lowercase for case-insensitive login."""
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()
        return username


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Choose a username', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md', 'required': True})
    )
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'placeholder': 'aayush@example.np', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md', 'required': True, 'type': 'email'})
    )
    experience_level = forms.ChoiceField(choices=User.EXPERIENCE_CHOICES, initial='beginner', widget=forms.HiddenInput)
    phone = forms.CharField(
        max_length=15,
        required=False,
        help_text='Optional. Phone number.',
        validators=[NEPALI_PHONE_REGEX],
        widget=forms.TextInput(attrs={'placeholder': '+977-98XXXXXXXX', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md pr-12', 'required': True})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md pr-12', 'required': True})
    )
    accept_terms = forms.BooleanField(
        required=True,
        label='I agree to the Terms of Service and Privacy Policy',
        widget=forms.CheckboxInput(attrs={'class': 'rounded border-outline text-primary focus:ring-primary h-5 w-5', 'id': 'terms'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'experience_level', 'accept_terms')

    def clean_email(self):
        """Normalize email to lowercase and allow reuse for unverified/inactive accounts."""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            existing = User.objects.filter(email__iexact=email).first()
            if existing:
                if existing.is_active and existing.email_verified:
                    raise forms.ValidationError('A user with this email already exists.')
        return email

    def clean_username(self):
        """Ensure username is unique (case-insensitive)."""
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('A user with this username already exists.')
        return username

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")
        return cleaned

    def save(self, commit=True):
        email = self.cleaned_data['email']
        user, created = User.objects.get_or_create(
            email__iexact=email,
            defaults={
                'username': self.cleaned_data['username'],
                'email': email,
                'phone': self.cleaned_data.get('phone', ''),
                'experience_level': self.cleaned_data.get('experience_level', 'beginner'),
                'skill_credits': 0,
                'beginner_tokens': 5,
                'is_active': False,
                'email_verified': False,
            },
        )
        if not created:
            user.is_active = False
            user.email_verified = False
        if commit:
            user.save()
        return user


class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit code',
            'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md text-center tracking-widest',
            'maxlength': '6',
            'inputmode': 'numeric',
            'pattern': '[0-9]{6}',
            'autocomplete': 'one-time-code',
        })
    )

    def clean_otp_code(self):
        code = self.cleaned_data.get('otp_code')
        if code and not code.isdigit():
            raise forms.ValidationError('Enter a valid 6-digit code.')
        return code


class UserProfileUpdateForm(UserChangeForm):
    password = forms.CharField(
        required=False,
        help_text='Leave blank to keep current password. Enter a new password to change it.',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New password (optional)',
            'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary',
            'autocomplete': 'new-password',
        })
    )
    password_confirm = forms.CharField(
        required=False,
        help_text='Confirm your new password.',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm new password',
            'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary',
            'autocomplete': 'new-password',
        })
    )

    class Meta:
        model = User
        fields = ('title', 'bio', 'profile_picture', 'phone', 'experience_level', 'password', 'password_confirm')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary'}),
        }

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get('password')
        pwd2 = cleaned.get('password_confirm')
        if pwd and not pwd2:
            self.add_error('password_confirm', 'Please confirm your new password.')
        elif pwd2 and not pwd:
            self.add_error('password', 'Please enter a new password.')
        elif pwd and pwd2 and pwd != pwd2:
            self.add_error('password_confirm', 'Passwords do not match.')
        else:
            instance = getattr(self, 'instance', None)
            if pwd and instance and getattr(instance, 'pk', None):
                if check_password(pwd, instance.password):
                    self.add_error('password', 'New password must be different from your current password.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user