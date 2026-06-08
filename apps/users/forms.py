from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
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
        """Normalize email to lowercase and check for duplicates (case-insensitive)."""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            if User.objects.filter(email__iexact=email).exists():
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
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        user.experience_level = self.cleaned_data.get('experience_level', 'beginner')
        user.skill_credits = 0
        user.beginner_tokens = 5
        if commit:
            user.save()
        return user


class UserProfileUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('bio', 'profile_picture', 'phone', 'experience_level')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'w-full'}),
        }