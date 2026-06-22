from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.cache import cache
from apps.skills.models import Skill
from apps.careers.models import CareerPath

User = get_user_model()


class CareerRecommendationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.skill1 = Skill.objects.create(name='Python', category='Programming')
        self.skill2 = Skill.objects.create(name='JavaScript', category='Programming')
        self.skill3 = Skill.objects.create(name='React', category='Frontend')
        self.skill4 = Skill.objects.create(name='Django', category='Backend')
        self.skill5 = Skill.objects.create(name='AWS', category='Cloud')

    def test_unauthenticated_redirect(self):
        response = self.client.get('/career/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_empty_recommendations_without_skills(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/career/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No recommendations available', response.content)

    def test_career_recommendations_content(self):
        career = CareerPath.objects.create(
            title='Full-Stack Developer',
            description='Build full stack apps',
            category='Technology',
            average_salary='NPR 1,500,000',
            growth_outlook='+28% YoY',
        )
        career.required_skills.add(self.skill1, self.skill2, self.skill3, self.skill4)

        self.user.teachable_skills.create(skill=self.skill1, proficiency_level='intermediate', hourly_commitment=5, is_active=True)
        self.user.teachable_skills.create(skill=self.skill2, proficiency_level='beginner', hourly_commitment=2, is_active=True)
        self.user.teachable_skills.create(skill=self.skill3, proficiency_level='expert', hourly_commitment=8, is_active=True)

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/career/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Full-Stack Developer', response.content)
        self.assertIn(b'Python', response.content)
        self.assertIn(b'JavaScript', response.content)
        self.assertIn(b'React', response.content)
        self.assertIn(b'Django', response.content)
        self.assertIn('75%', response.content.decode())

    def test_cache_served_on_repeated_requests(self):
        CareerPath.objects.create(
            title='Data Scientist',
            description='Analyze data',
            category='Data',
            average_salary='NPR 1,800,000',
            growth_outlook='+35% YoY',
        ).required_skills.add(self.skill1)

        self.user.teachable_skills.create(skill=self.skill1, proficiency_level='intermediate', hourly_commitment=4, is_active=True)

        self.client.login(username='testuser', password='testpass123')
        response1 = self.client.get('/career/')
        cache_key = f'career_recommendations_{self.user.id}'
        self.assertTrue(cache.get(cache_key) is not None)

    def test_refresh_clears_cache(self):
        cache_key = f'career_recommendations_{self.user.id}'
        cache.set(cache_key, {'recommendations': [], 'from_cache': True}, timeout=60 * 60 * 24)

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/career/refresh/')
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(cache.get(cache_key))

    def test_api_returns_json(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/career/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertIn('recommendations', data)
        self.assertIn('count', data)

    def test_api_unauthenticated_returns_401(self):
        response = self.client.get('/career/api/')
        self.assertEqual(response.status_code, 401)


class CareerRegressionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='reguser',
            email='reg@example.com',
            password='regpass123'
        )

    def test_exchange_partners_page_loads(self):
        response = self.client.get('/exchanges/partners/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='reguser', password='regpass123')
        response = self.client.get('/exchanges/partners/')
        self.assertEqual(response.status_code, 200)
