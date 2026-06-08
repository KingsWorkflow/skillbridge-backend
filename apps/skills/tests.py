from django.test import TestCase
from apps.skills.models import Skill, TeachableSkill, LearnableSkill
from django.contrib.auth import get_user_model

User = get_user_model()


class SkillsTest(TestCase):
    def setUp(self):
        self.python = Skill.objects.create(name='Python', category='Programming')
        self.design = Skill.objects.create(name='UI Design', category='Design')

    def test_unique_skill_names(self):
        self.assertEqual(Skill.objects.filter(name='Python').count(), 1)