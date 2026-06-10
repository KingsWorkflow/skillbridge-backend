from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.skills.models import Skill, TeachableSkill, LearnableSkill
from apps.exchanges.models import ExchangeProposal, ExchangeSession, SkillCreditTransaction
from apps.verification.models import SkillVerification, Certificate
from apps.portfolio.models import Project, Certification as PortfolioCertification
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

SKILLS = [
    ("Python", "Programming"), ("Django", "Programming"), ("React", "Frontend"),
    ("UI/UX Design", "Design"), ("Data Analysis", "Data"), ("Digital Marketing", "Marketing"),
    ("Graphic Design", "Design"), ("Photography", "Media"), ("Content Writing", "Media"),
    ("SEO", "Marketing"), ("AWS", "Cloud"), ("Docker", "DevOps"),
    ("Machine Learning", "Data"), ("Flutter", "Mobile"), ("Video Editing", "Media"),
]

USERS = [
    ("alice", "alice@example.com", "Testpass123!", "intermediate"),
    ("bob", "bob@example.com", "Testpass123!", "beginner"),
    ("carol", "carol@example.com", "Testpass123!", "advanced"),
    ("david", "david@example.com", "Testpass123!", "intermediate"),
    ("eve", "eve@example.com", "Testpass123!", "beginner"),
    ("frank", "frank@example.com", "Testpass123!", "advanced"),
]

class Command(BaseCommand):
    help = "Seed demo data for SkillBridge"

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # Skills
        skill_objs = []
        for name, category in SKILLS:
            skill, _ = Skill.objects.get_or_create(name=name, defaults={"category": category, "popularity_score": round(random.uniform(1, 10), 1)})
            skill_objs.append(skill)
        self.stdout.write(f"Skills: {Skill.objects.count()}")

        # Users
        user_objs = []
        for username, email, password, level in USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "experience_level": level, "skill_credits": random.randint(0, 50), "beginner_tokens": random.randint(0, 10)},
            )
            if created:
                user.set_password(password)
                user.save()
            user_objs.append(user)
        self.stdout.write(f"Users: {User.objects.count()}")

        # Teachable / Learnable skills
        for user in user_objs:
            for skill in random.sample(skill_objs, k=random.randint(2, 4)):
                TeachableSkill.objects.get_or_create(
                    user=user, skill=skill,
                    defaults={"proficiency_level": random.choice(["beginner", "intermediate", "expert"]), "hourly_commitment": random.randint(1, 10), "is_active": True},
                )
                LearnableSkill.objects.get_or_create(
                    user=user, skill=skill,
                    defaults={"urgency": random.choice(["low", "medium", "high"])},
                )
        self.stdout.write(f"TeachableSkills: {TeachableSkill.objects.count()}")
        self.stdout.write(f"LearnableSkills: {LearnableSkill.objects.count()}")

        # Skill verifications
        for user in user_objs[:3]:
            for skill in random.sample(skill_objs, k=2):
                SkillVerification.objects.get_or_create(
                    user=user, skill=skill,
                    defaults={"current_level": random.randint(0, 3), "verification_votes": random.randint(0, 5), "total_teaching_hours": random.randint(0, 20), "average_rating": round(random.uniform(0, 5), 1)},
                )
        self.stdout.write(f"SkillVerifications: {SkillVerification.objects.count()}")

        # Certificates
        for user in user_objs[:3]:
            for skill in random.sample(skill_objs, k=1):
                Certificate.objects.get_or_create(
                    user=user, skill=skill,
                    defaults={"issuing_organization": "SkillBridge Academy", "issue_date": timezone.now().date() - timedelta(days=random.randint(1, 30)), "status": random.choice(["pending", "approved", "rejected"])},
                )
        self.stdout.write(f"Certificates: {Certificate.objects.count()}")

        # Exchange proposals
        for _ in range(5):
            proposer, receiver = random.sample(user_objs, 2)
            offer_skill = random.choice(proposer.teachable_skills.all())
            learnable_skills = receiver.learnable_skills.all()
            if not learnable_skills.exists():
                continue
            request_skill = random.choice(learnable_skills)
            ExchangeProposal.objects.get_or_create(
                proposer=proposer, receiver=receiver, offer_skill=offer_skill, request_skill=request_skill,
                defaults={"proposed_hours": random.randint(1, 10), "message": "Let's exchange skills!", "status": random.choice(["pending", "accepted", "rejected"])},
            )
        self.stdout.write(f"ExchangeProposals: {ExchangeProposal.objects.count()}")

        # Sessions
        for proposal in ExchangeProposal.objects.filter(status="accepted"):
            if not ExchangeSession.objects.filter(proposal=proposal).exists():
                ExchangeSession.objects.create(
                    proposal=proposal,
                    scheduled_date=timezone.now() + timedelta(days=random.randint(1, 14)),
                    duration_hours=random.randint(1, 3),
                    meeting_link="https://meet.example.com/" + str(random.randint(1000, 9999)),
                    teacher=proposal.offer_skill.user,
                    learner=proposal.request_skill.user,
                    skill_taught=proposal.offer_skill.skill,
                    completed=random.choice([True, False]),
                )
        self.stdout.write(f"ExchangeSessions: {ExchangeSession.objects.count()}")

        # Transactions
        for session in ExchangeSession.objects.filter(completed=True):
            SkillCreditTransaction.objects.get_or_create(
                user=session.teacher,
                amount=10 * session.duration_hours,
                transaction_type="teach_earn",
                description=f"Taught {session.duration_hours} hours of {session.skill_taught.name}",
                related_session=session,
            )
            SkillCreditTransaction.objects.get_or_create(
                user=session.learner,
                amount=-10 * session.duration_hours,
                transaction_type="learn_spend",
                description=f"Learned {session.duration_hours} hours of {session.skill_taught.name}",
                related_session=session,
            )
        self.stdout.write(f"SkillCreditTransactions: {SkillCreditTransaction.objects.count()}")

        # Portfolio projects
        for user in user_objs:
            for _ in range(random.randint(1, 3)):
                Project.objects.get_or_create(
                    user=user,
                    title=f"{user.username}'s Project {_}",
                    defaults={"description": "A demo project showcasing skills.", "project_url": "https://github.com/example"},
                )
        self.stdout.write(f"Projects: {Project.objects.count()}")

        # Portfolio certifications
        for user in user_objs[:3]:
            for skill in random.sample(skill_objs, k=1):
                PortfolioCertification.objects.get_or_create(
                    user=user, name=skill.name,
                    defaults={"issuing_organization": "SkillBridge", "issue_date": timezone.now().date() - timedelta(days=random.randint(1, 60))},
                )
        self.stdout.write(f"PortfolioCertifications: {PortfolioCertification.objects.count()}")

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully!"))
