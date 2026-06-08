from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, datetime
import csv
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.users.models import UserProfile
from apps.skills.models import Skill, TeachableSkill, LearnableSkill
from apps.exchanges.models import ExchangeProposal, ExchangeSession, SkillCreditTransaction
from apps.verification.models import Certificate, SkillVerification, SkillExam, ExamAttempt
from apps.portfolio.models import Project, Certification


User = get_user_model()


class AdminAnalyticsDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True,
        )
        self.normal_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpass123',
            is_staff=False,
        )

    def test_analytics_requires_staff(self):
        url = reverse('admin:analytics_dashboard')
        response = self.client.get(url)
        self.assertRedirects(response, '/admin/login/?next=/admin/analytics/')

    def test_analytics_accessible_by_staff(self):
        self.client.force_login(self.staff_user)
        url = reverse('admin:analytics_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Total Users', str(response.content))


class AdminBulkVerifyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True,
        )

    def test_bulk_verify_requires_staff(self):
        url = reverse('admin:bulk_verify')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_bulk_verify_get(self):
        self.client.force_login(self.staff_user)
        url = reverse('admin:bulk_verify')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_bulk_verify_post_valid_csv(self):
        skill = Skill.objects.create(name='Python', category='Programming')
        user = UserProfile.objects.create_user(
            username='piuser',
            email='piuser@example.com',
            password='testpass123',
        )
        self.client.force_login(self.staff_user)
        url = reverse('admin:bulk_verify')
        csv_content = "email,skill_name\npiuser@example.com,Python\n"
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode(), content_type="text/csv")
        response = self.client.post(url, {'csv_file': csv_file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Certificate.objects.count(), 1)
        self.assertEqual(Certificate.objects.first().status, 'approved')

    def test_bulk_verify_post_invalid_csv_extension(self):
        self.client.force_login(self.staff_user)
        url = reverse('admin:bulk_verify')
        csv_file = SimpleUploadedFile("test.txt", b"", content_type="text/plain")
        response = self.client.post(url, {'csv_file': csv_file})
        self.assertEqual(response.status_code, 302)


class AdminModelAdminActionTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.staff_user)

    def test_user_activation_action(self):
        user1 = UserProfile.objects.create_user(username='u1', email='u1@e.com', password='test')
        user2 = UserProfile.objects.create_user(username='u2', email='u2@e.com', password='test')
        url = reverse('admin:users_userprofile_changelist')
        response = self.client.post(url, {'action': 'activate_users', '_selected_action': [user1.pk, user2.pk]})
        user1.refresh_from_db()
        user2.refresh_from_db()
        self.assertTrue(user1.is_active)
        self.assertTrue(user2.is_active)

    def test_certificate_approve_action(self):
        skill = Skill.objects.create(name='Java', category='Programming')
        user = UserProfile.objects.create_user(username='certuser', email='cert@e.com', password='test')
        cert = Certificate.objects.create(
            user=user,
            skill=skill,
            issuing_organization='Org',
            issue_date=timezone.now().date(),
            status='pending',
        )
        url = reverse('admin:verification_certificate_changelist')
        response = self.client.post(url, {'action': 'approve_certificates', '_selected_action': [cert.pk]})
        cert.refresh_from_db()
        self.assertEqual(cert.status, 'approved')
        self.assertIsNotNone(cert.verified_at)

    def test_exchange_mark_accepted_action(self):
        proposer = UserProfile.objects.create_user(username='p1', email='p1@e.com', password='test')
        receiver = UserProfile.objects.create_user(username='r1', email='r1@e.com', password='test')
        skill = Skill.objects.create(name='C++', category='Programming')
        ts = TeachableSkill.objects.create(user=proposer, skill=skill, proficiency_level='intermediate', hourly_commitment=2)
        ls = LearnableSkill.objects.create(user=receiver, skill=skill, urgency='medium')
        proposal = ExchangeProposal.objects.create(
            proposer=proposer,
            receiver=receiver,
            offer_skill=ts,
            request_skill=ls,
            proposed_hours=5,
            status='pending',
        )
        url = reverse('admin:exchanges_exchangeproposal_changelist')
        response = self.client.post(url, {'action': 'mark_accepted', '_selected_action': [proposal.pk]})
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')

    def test_verification_level_action(self):
        skill = Skill.objects.create(name='Ruby', category='Programming')
        user = UserProfile.objects.create_user(username='vuser', email='v@e.com', password='test')
        sv = SkillVerification.objects.create(user=user, skill=skill, current_level=2, verification_votes=5)
        url = reverse('admin:verification_skillverification_changelist')
        response = self.client.post(url, {'action': 'increase_level', '_selected_action': [sv.pk]})
        sv.refresh_from_db()
        self.assertEqual(sv.current_level, 3)
