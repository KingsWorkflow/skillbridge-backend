from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    phone = forms.CharField(max_length=15, required=False, help_text='Optional. Phone number.')
    experience_level = forms.ChoiceField(choices=User.EXPERIENCE_CHOICES, initial='beginner')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'experience_level')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class UserProfileUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('bio', 'profile_picture', 'phone', 'experience_level')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'w-full'}),
        }