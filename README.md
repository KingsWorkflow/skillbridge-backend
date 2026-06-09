# SkillBridge — Backend & Admin Documentation

AI-powered career guidance and skill exchange platform for students and young professionals.

**Stack:** Python · Django · PostgreSQL · django-admin-interface · scikit-learn

---

## Project Overview

SkillBridge is a web-based skill exchange platform with an intelligent recommendation engine. Users can teach skills they have and learn skills they want — no money involved.

### Core Features
- JWT authentication
- AI career recommendations and skill gap analysis
- Peer-to-peer skill exchange with credit economy
- Skill verification (certificates, exams, community votes)
- Portfolio management
- Modern admin dashboard with analytics

---

## Objectives
- Personalized career path suggestions based on user skills
- Skill gap analysis against industry requirements
- Peer-to-peer skill exchange without monetary transactions
- Skill verification with 5 trust levels
- Professional portfolio tools
- Analytics-driven admin panel

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Framework | Django 6.x |
| Database | PostgreSQL 14+ |
| Auth | djangorestframework-simplejwt |
| ML/AI | scikit-learn, pandas, numpy |
| Admin UI | django-admin-interface, django-colorfield |
| API Docs | drf-yasg (Swagger) |
| CORS | django-cors-headers |
| Env | python-dotenv |

---

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip
- Git

---

## Local Setup

```bash
git clone https://github.com/your-org/skillbridge-backend.git
cd skillbridge-backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

| Service | URL |
|---------|-----|
| API Root | `http://localhost:8000/api/` |
| Admin Panel | `http://localhost:8000/admin/` |
| Swagger Docs | `http://localhost:8000/swagger/` |

---

## Environment Variables

```env
SECRET_KEY=your-super-secret-key-minimum-50-characters
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=skillbridge_db
DB_USER=skillbridge_user
DB_PASSWORD=yourpassword123
DB_HOST=localhost
DB_PORT=5432

JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=86400
CORS_ALLOWED_ORIGINS=http://localhost:3000

DEFAULT_BEGINNER_TOKENS=5
SKILL_CREDIT_EARN_RATE=10
SKILL_CREDIT_SPEND_RATE=10

COMMUNITY_VERIFICATION_THRESHOLD=3
EXPERT_TEACHING_HOURS_THRESHOLD=50
```

---

## Database Setup

```bash
psql -U postgres
CREATE DATABASE skillbridge_db;
CREATE USER skillbridge_user WITH PASSWORD 'yourpassword123';
ALTER ROLE skillbridge_user SET client_encoding TO 'utf8';
ALTER ROLE skillbridge_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE skillbridge_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE skillbridge_db TO skillbridge_user;
\q

python manage.py makemigrations users skills exchanges recommendations verification portfolio
python manage.py migrate
```

---

## Project Structure

```
skillbridge-backend/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── venv/
├── skillbridge/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/               # Auth, profiles, credits
│   ├── skills/              # Skill catalog, teachable/learnable skills
│   ├── exchanges/           # Proposals, sessions, transactions
│   ├── recommendations/     # AI matching engine
│   ├── verification/        # Certificates, exams, attempts
│   ├── portfolio/           # Projects, certifications
│   └── admin_custom/        # Custom admin dashboard & views
├── templates/
│   └── admin_custom/        # Analytics + bulk verify templates
└── static/
```

---

## Database Models

### UserProfile (extends AbstractUser)
- `username`, `email`, `phone`, `bio`
- `experience_level`: beginner / intermediate / advanced
- `skill_credits`, `beginner_tokens`, `reputation_score`
- `total_hours_taught`, `total_hours_learned`

### Skill
- `name` (unique), `category`, `popularity_score`

### TeachableSkill
- `user` → UserProfile
- `skill` → Skill
- `proficiency_level`, `hourly_commitment`, `is_active`

### LearnableSkill
- `user` → UserProfile
- `skill` → Skill
- `motivation`, `urgency`

### ExchangeProposal
- `proposer`, `receiver` → UserProfile
- `offer_skill` → TeachableSkill
- `request_skill` → LearnableSkill
- `proposed_hours`, `status`, `message`

### ExchangeSession
- `proposal` → ExchangeProposal
- `scheduled_date`, `duration_hours`, `meeting_link`
- `teacher`, `learner` → UserProfile
- `completed`, ratings, feedback

### SkillCreditTransaction
- `user` → UserProfile
- `amount`, `transaction_type`, `description`, `related_session`

### SkillVerification
- `user`, `skill`
- `current_level` (0-5), `verification_votes`
- Timestamps for each verification method

### Certificate
- `user`, `skill`
- `certificate_file`, `issuing_organization`, `issue_date`
- `status`: pending / approved / rejected

### SkillExam
- `skill`, `difficulty`, `title`
- `time_limit_minutes`, `passing_score`, `questions`
- `is_active`

### ExamAttempt
- `user`, `exam`
- `score`, `passed`, `answers`
- `completed_at`, `can_retake_after`

---

## Verification Levels

| Level | Badge | Requirement |
|-------|-------|-------------|
| 1 | Self-Declared | Add skill to profile |
| 2 | Community Verified | 3+ peer verifications |
| 3 | Certificate Verified | Admin-approved certificate |
| 4 | Platform Tested | Pass on-site exam |
| 5 | Expert | Level 4 + 50+ teaching hours + high rating |

---

## Credit Economy

| Action | Change |
|--------|--------|
| Sign up | +5 beginner tokens |
| Teach 1 hour | +10 credits |
| Learn 1 hour | -10 credits |
| Refer a friend | +5 credits |
| Leave feedback | +1 credit |
| Verify another user | +2 credits |

---

## Admin Panel

Custom analytics-driven admin built on django-admin-interface.

**Routes:**
- `/admin/` — enhanced dashboard
- `/admin/analytics/` — charts + KPIs
- `/admin/bulk-verify/` — CSV bulk certificate approval

**ModelAdmin enhancements across all apps:**
- `list_display`, `list_filter`, `search_fields`, `date_hierarchy`
- Custom actions with confirmation dialogs
- `list_select_related` / `prefetch_related` for query optimization
- Tabular inlines for related models

---

## Testing

```bash
# All tests (24 tests across apps + admin custom)
python manage.py test

# Specific app
python manage.py test apps.exchanges
python manage.py test apps.verification
python manage.py test apps.users

# With coverage
pip install coverage
coverage run manage.py test
coverage report
```

Target coverage: 90%+ on exchanges, verification, and admin custom views.

---

## Deployment

### Render (Free Tier)
- Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start: `gunicorn skillbridge.wsgi:application`
- Attach PostgreSQL add-on

### Production Checklist
- `DEBUG=False`
- Strong `SECRET_KEY`
- `ALLOWED_HOSTS` set
- PostgreSQL attached
- CORS configured
- Email configured
- Certificate storage (S3 or similar)

---

## Common Issues

```bash
# Reset migrations (dev only)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate

# System checks
python manage.py check

# Full suite
python manage.py test
```

---

*SkillBridge — AI-Powered Skill Exchange Platform*
