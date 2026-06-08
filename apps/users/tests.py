from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.skills.models import Skill, TeachableSkill, LearnableSkill
from apps.users.forms import CustomUserCreationForm

User = get_user_model()


class RegistrationTestCase(TestCase):
    def test_registration_form_valid(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2024',
            'phone': '+977-9841234567',
            'experience_level': 'beginner'
        })
        self.assertTrue(form.is_valid())

    def test_registration_creates_user(self):
        response = self.client.post(reverse('users:register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Str0ng!Pass#2024',
            'password2': 'Str0ng!Pass#2024',
            'phone': '+977-9841234567',
            'experience_level': 'beginner'
        })
        self.assertRedirects(response, reverse('users:dashboard'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_has_correct_defaults(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.assertEqual(user.skill_credits, 0)
        self.assertEqual(user.beginner_tokens, 5)
        self.assertEqual(user.experience_level, 'beginner')


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

    def test_learnable_skill(self):
        user = User.objects.create_user(username='learner', email='learner@example.com')
        learnable = LearnableSkill.objects.create(
            user=user,
            skill=self.skill,
            urgency='high'
        )
        self.assertEqual(str(learnable), f"{user} wants to learn {self.skill}")