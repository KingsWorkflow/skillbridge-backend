from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'w-full pl-12 pr-12 py-4 bg-surface-container-low border border-on-surface/10 rounded-lg focus:ring-2 focus:ring-secondary/20 focus:border-secondary outline-none transition-all font-body-md text-body-md', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'w-full pl-12 pr-12 py-4 bg-surface-container-low border border-on-surface/10 rounded-lg focus:ring-2 focus:ring-secondary/20 focus:border-secondary outline-none transition-all font-body-md text-body-md'})
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Choose a username', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md'})
    )
    email = forms.EmailField(
        required=True, 
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'placeholder': 'aayush@example.np', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md'})
    )
    experience_level = forms.ChoiceField(choices=User.EXPERIENCE_CHOICES, initial='beginner', widget=forms.HiddenInput)
    phone = forms.CharField(
        max_length=15, 
        required=False, 
        help_text='Optional. Phone number.',
        widget=forms.TextInput(attrs={'placeholder': '+977-98XXXXXXXX', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md pr-12'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'w-full bg-surface-container-lowest border-0 border-b-2 border-outline-variant focus:border-secondary focus:ring-0 transition-all px-0 py-2 font-body-md text-body-md pr-12'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'experience_level')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

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