from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.skills.models import Skill, TeachableSkill, LearnableSkill
from apps.users.forms import CustomUserCreationForm, CustomAuthenticationForm

User = get_user_model()


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='Existing@Example.com',
            password='password123'
        )

    def test_registration_form_valid(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'Test@Example.com',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2024',
            'phone': '+977-9841234567',
            'experience_level': 'beginner',
            'accept_terms': True,
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.experience_level, 'beginner')
        self.assertEqual(user.skill_credits, 0)
        self.assertEqual(user.beginner_tokens, 5)
        self.assertEqual(user.email, 'test@example.com')

    def test_registration_rejects_duplicate_email_case_insensitive(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser2',
            'email': 'EXISTING@EXAMPLE.COM',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2024',
            'experience_level': 'intermediate',
            'accept_terms': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registration_rejects_duplicate_username(self):
        form = CustomUserCreationForm(data={
            'username': 'EXISTINGUSER',
            'email': 'new@example.com',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2024',
            'experience_level': 'beginner',
            'accept_terms': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_registration_rejects_weak_password(self):
        form = CustomUserCreationForm(data={
            'username': 'weakpassuser',
            'email': 'weak@example.com',
            'password1': 'short',
            'password2': 'short',
            'experience_level': 'beginner',
            'accept_terms': True,
        })
        self.assertFalse(form.is_valid())

    def test_registration_rejects_mismatched_passwords(self):
        form = CustomUserCreationForm(data={
            'username': 'mismatchuser',
            'email': 'mismatch@example.com',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2025',
            'experience_level': 'beginner',
            'accept_terms': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_registration_rejects_unchecked_terms(self):
        form = CustomUserCreationForm(data={
            'username': 'noterms',
            'email': 'noterms@example.com',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2024',
            'experience_level': 'beginner',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('accept_terms', form.errors)

    def test_registration_phone_invalid_format(self):
        form = CustomUserCreationForm(data={
            'username': 'phoneuser',
            'email': 'phoneuser@example.com',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2024',
            'phone': '12345',
            'experience_level': 'beginner',
            'accept_terms': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_registration_phone_valid_nepali(self):
        form = CustomUserCreationForm(data={
            'username': 'phoneuser2',
            'email': 'phoneuser2@example.com',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2024',
            'phone': '9812345678',
            'experience_level': 'beginner',
            'accept_terms': True,
        })
        self.assertTrue(form.is_valid())

    def test_registration_phone_optional_blank(self):
        form = CustomUserCreationForm(data={
            'username': 'nophone',
            'email': 'nophone@example.com',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2024',
            'experience_level': 'beginner',
            'accept_terms': True,
        })
        self.assertTrue(form.is_valid())

    def test_login_email_case_insensitive(self):
        form = CustomAuthenticationForm(data={
            'username': 'existing@example.com',
            'password': 'password123'
        })
        self.assertTrue(form.is_valid())

        form = CustomAuthenticationForm(data={
            'username': 'EXISTING@EXAMPLE.COM',
            'password': 'password123'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('username'), 'existing@example.com')

    def tearDown(self):
        User.objects.filter(username__in=[
            'existinguser', 'testuser', 'testuser2', 'weakpassuser',
            'mismatchuser', 'noterms', 'phoneuser', 'phoneuser2', 'nophone'
        ]).delete()


class SkillTestCase(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name='Python', category='Programming')

    def test_skill_creation(self):
        self.assertEqual(str(self.skill), 'Python')

    def test_teachable_skill(self):
        user = User.objects.create_user(username='teacher', email='teacher@example.com')
        teachable = TeachableSkill.objects.create(
            user=user,
            skill=self.skill,
            proficiency_level='intermediate',
            hourly_commitment=5
        )
        self.assertEqual(str(teachable), f"{user} teaches {self.skill}")
        user.delete()

    def test_learnable_skill(self):
        user = User.objects.create_user(username='learner', email='learner@example.com')
        learnable = LearnableSkill.objects.create(
            user=user,
            skill=self.skill,
            urgency='high'
        )
        self.assertEqual(str(learnable), f"{user} wants to learn {self.skill}")
        user.delete()