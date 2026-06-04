# SkillBridge — Backend API Documentation

> AI-powered career guidance and **skill exchange platform** for students and young professionals worldwide.  
> *Peer-to-peer skill sharing · No money involved · Free for everyone*

**Stack:** Django 5.x · Django REST Framework · PostgreSQL 14+ · scikit-learn · JWT Auth

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Objectives](#objectives)
4. [Tech Stack](#tech-stack)
5. [Prerequisites](#prerequisites)
6. [Local Setup](#local-setup)
7. [Environment Variables](#environment-variables)
8. [Database Setup](#database-setup)
9. [Running the Server](#running-the-server)
10. [Project Structure](#project-structure)
11. [Database Models](#database-models)
12. [API Endpoints](#api-endpoints)
13. [AI Recommendation Engine](#ai-recommendation-engine)
14. [Skill Exchange System](#skill-exchange-system)
15. [Skill Verification System](#skill-verification-system)
16. [Authentication](#authentication)
17. [Admin Panel](#admin-panel)
18. [Testing](#testing)
19. [Deployment](#deployment)
20. [Common Issues & Fixes](#common-issues--fixes)

---

## Project Overview

**SkillBridge** is a web-based platform where AI-guided career counseling meets a **skill-sharing ecosystem**. The backend exposes a RESTful API consumed by the React frontend.

### Core Features

| Feature | Description |
|---------|-------------|
| **JWT Authentication** | User registration, login, profile management |
| **AI Career Recommendations** | TF-IDF + Cosine Similarity to suggest career paths based on user skills |
| **Skill Gap Analysis** | Compares user skills vs. target career requirements |
| **Learning Roadmap Generation** | Ordered stages to acquire missing skills |
| **Peer-to-Peer Skill Exchange** | Offer skills you have, request skills you want to learn — **no money involved** |
| **Exchange Proposal System** | Send/accept/reject skill exchange requests |
| **Session Booking** | Schedule and rate skill exchange sessions |
| **Skill Verification** | Certificate upload, on-site exams, community verification (5 trust levels) |
| **Portfolio Management** | Showcase projects and certifications |
| **Admin Panel** | User management, platform analytics, skill moderation |

### Platform Philosophy

> *"Everyone has something to teach. Everyone has something to learn. No money required."*

- **Pure learners** (no skills to offer) earn credits through referrals, feedback, or community contributions
- **Skill credits** system ensures fair exchange without currency
- **Beginner tokens** (5 free on signup) let anyone start learning immediately
- **Verification badges** (5 levels) build trust in skill claims

---

## Problem Statement

The major issues that motivated this project are:

| Problem | Description |
|---------|-------------|
| **Skills-Industry Gap** | Graduates often lack skills required by the job market, resulting in high unemployment or underemployment |
| **Lack of Personalized Guidance** | Limited access to quality career counseling and awareness of available opportunities |
| **Poor Peer Learning Infrastructure** | No formal structure to share skills and encourage collaborative learning |
| **Information Asymmetry** | Students lack access to current information about in-demand skills and industry trends |
| **Limited Portfolio Tools** | Students lack tools to create professional portfolios showcasing projects and certifications |
| **Financial Barriers** | Expensive courses and training programs are inaccessible to many |

These issues limit professional development and decrease human capital productivity. SkillBridge directly addresses these problem dimensions through an integrated digital platform.

---

## Objectives

### Main Objective

To provide a web-based system with an intelligent skill recommendation engine that enables students and young professionals to explore suitable career paths, identify skill gaps, and exchange skills with peers — all without monetary transactions.

### Specific Objectives

| # | Objective |
|---|-----------|
| 1 | Provide personalized career path suggestions based on user skills, interests, and goals |
| 2 | Identify gaps between user skills and industry requirements for desired careers |
| 3 | Build a skill exchange platform enabling users to gain and give skills without monetary exchange |
| 4 | Raise awareness about career trends, internships, and in-demand skills |
| 5 | Help users build professional portfolios to display projects and certifications |
| 6 | Foster peer-to-peer learning, networking, and collaboration |
| 7 | Bridge the gap between academic learning and real-world requirements |

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.10+ |
| Web Framework | Django | 5.x |
| REST API | Django REST Framework | 3.15+ |
| Database | PostgreSQL | 14+ |
| Authentication | djangorestframework-simplejwt | latest |
| AI / ML | scikit-learn, pandas, numpy | latest |
| API Documentation | drf-yasg (Swagger) | latest |
| CORS | django-cors-headers | latest |
| Environment | python-dotenv | latest |
| Deployment | Render + Gunicorn | — |

---

## Prerequisites

Make sure the following are installed:

- **Python 3.10+** — [python.org](https://python.org)
- **PostgreSQL 14+** — [postgresql.org](https://postgresql.org)
- **pip** (comes with Python)
- **Git**

Verify installations:

```bash
python --version       # Python 3.10+
psql --version         # psql 14+
pip --version
git --version
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-org/skillbridge-backend.git
cd skillbridge-backend
```

### 2. Create and activate virtual environment

```bash
# Create
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```bash
cp .env.example .env
```

Edit `.env` with your local values (see [Environment Variables](#environment-variables)).

### 5. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser (admin)

```bash
python manage.py createsuperuser
```

### 7. (Optional) Load seed data

```bash
python manage.py loaddata fixtures/initial_skills.json
python manage.py loaddata fixtures/initial_users.json
```

### 8. Start development server

```bash
python manage.py runserver
```

| Service | URL |
|---------|-----|
| API Root | `http://localhost:8000/api/` |
| Admin Panel | `http://localhost:8000/admin/` |
| Swagger Docs | `http://localhost:8000/swagger/` |

---

## Environment Variables

Create `.env` in project root. **Never commit this file.**

```env
# Django
SECRET_KEY=your-super-secret-key-minimum-50-characters
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=skillbridge_db
DB_USER=skillbridge_user
DB_PASSWORD=yourpassword123
DB_HOST=localhost
DB_PORT=5432

# JWT Token Lifetimes (seconds)
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=86400

# CORS (frontend origins)
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Skill Exchange System
DEFAULT_BEGINNER_TOKENS=5
SKILL_CREDIT_EARN_RATE=10
SKILL_CREDIT_SPEND_RATE=10

# Verification System
COMMUNITY_VERIFICATION_THRESHOLD=3
EXPERT_TEACHING_HOURS_THRESHOLD=50

# Email (optional for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

---

## Database Setup

### Create PostgreSQL database and user

```bash
# Connect to PostgreSQL
psql -U postgres

# Inside psql shell
CREATE DATABASE skillbridge_db;
CREATE USER skillbridge_user WITH PASSWORD 'yourpassword123';
ALTER ROLE skillbridge_user SET client_encoding TO 'utf8';
ALTER ROLE skillbridge_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE skillbridge_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE skillbridge_db TO skillbridge_user;
\q
```

### Run migrations

```bash
python manage.py makemigrations users skills exchanges recommendations verification portfolio
python manage.py migrate
```

---

## Running the Server

```bash
# Development
python manage.py runserver

# Custom port
python manage.py runserver 8080

# Accessible on local network
python manage.py runserver 0.0.0.0:8000
```

---

## Project Structure

```
skillbridge-backend/
│
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── Procfile
│
├── skillbridge/                 # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── apps/
    ├── users/                   # User profiles, auth
    ├── skills/                  # Skill catalog
    ├── exchanges/               # Core skill exchange system
    ├── recommendations/         # AI engine
    ├── verification/            # Skill verification system
    ├── portfolio/               # User portfolios
    └── notifications/           # In-app + email notifications
```

---

## Database Models

### UserProfile (extends AbstractUser)

| Field | Type | Description |
|-------|------|-------------|
| `username` | CharField | Unique handle |
| `email` | EmailField | Unique email |
| `phone` | CharField | Optional |
| `profile_picture` | ImageField | Avatar |
| `bio` | TextField | Short introduction |
| `experience_level` | CharField | `beginner` / `intermediate` / `advanced` |
| `skill_credits` | IntegerField | Earned by teaching (default: 0) |
| `beginner_tokens` | IntegerField | Free tokens for new users (default: 5) |
| `reputation_score` | FloatField | Average rating from completed exchanges |
| `total_hours_taught` | IntegerField | Lifetime teaching hours |
| `total_hours_learned` | IntegerField | Lifetime learning hours |

### Skill

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | e.g., "Python", "UI Design" |
| `category` | CharField | e.g., "Programming", "Design", "Language" |
| `popularity_score` | FloatField | Based on exchange frequency |

### TeachableSkill

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | → UserProfile |
| `skill` | ForeignKey | → Skill |
| `proficiency_level` | CharField | `beginner` / `intermediate` / `expert` |
| `hourly_commitment` | IntegerField | Hours per week available |
| `is_active` | BooleanField | Currently offering? |

### LearnableSkill

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | → UserProfile |
| `skill` | ForeignKey | → Skill |
| `motivation` | TextField | Why they want to learn |
| `urgency` | CharField | `low` / `medium` / `high` |

### ExchangeProposal

| Field | Type | Description |
|-------|------|-------------|
| `proposer` | ForeignKey | User making the offer |
| `receiver` | ForeignKey | User receiving the offer |
| `offer_skill` | ForeignKey | → TeachableSkill |
| `request_skill` | ForeignKey | → LearnableSkill |
| `proposed_hours` | IntegerField | Total hours for exchange |
| `status` | CharField | `pending` / `accepted` / `rejected` / `completed` / `cancelled` |
| `message` | TextField | Optional note |

### ExchangeSession

| Field | Type | Description |
|-------|------|-------------|
| `proposal` | ForeignKey | → ExchangeProposal |
| `scheduled_date` | DateTimeField | When session occurs |
| `duration_hours` | IntegerField | Length of session |
| `meeting_link` | URLField | Google Meet / Zoom link |
| `completed` | BooleanField | Session finished? |
| `teacher_rating` | IntegerField | 1-5 (rated by learner) |
| `learner_rating` | IntegerField | 1-5 (rated by teacher) |

### SkillCreditTransaction

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | → UserProfile |
| `amount` | IntegerField | Positive = earned, Negative = spent |
| `transaction_type` | CharField | `teach_earn` / `learn_spend` / `signup_bonus` / `referral_bonus` |
| `description` | TextField | Transaction details |

### SkillVerification (5 Trust Levels)

| Level | Badge | Meaning | Requirement |
|-------|-------|---------|-------------|
| 0 | — | Unverified | Default |
| 1 | 📝 | Self-Declared | Added to profile |
| 2 | 👍 | Community Verified | 3+ peer verifications |
| 3 | 🎓 | Certificate Verified | Approved certificate |
| 4 | ✅ | Platform Tested | Pass on-site exam (80%+) |
| 5 | ⭐ | Expert | Level 4 + 50+ teaching hours + 4.8+ rating |

### Certificate

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | → UserProfile |
| `skill` | ForeignKey | → Skill |
| `certificate_file` | FileField | Uploaded PDF/image |
| `issuing_organization` | CharField | e.g., "Coursera" |
| `status` | CharField | `pending` / `approved` / `rejected` |

### SkillExam

| Field | Type | Description |
|-------|------|-------------|
| `skill` | ForeignKey | → Skill |
| `difficulty` | CharField | `beginner` / `intermediate` / `advanced` |
| `time_limit_minutes` | IntegerField | Default 30 |
| `passing_score` | IntegerField | Default 70 |
| `questions` | JSONField | List of question objects |

### ExamAttempt

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | → UserProfile |
| `exam` | ForeignKey | → SkillExam |
| `score` | FloatField | Percentage score |
| `passed` | BooleanField | Met passing score? |
| `can_retake_after` | DateTimeField | 14-day cooldown if failed |

---

## API Endpoints

All endpoints prefixed with `/api/`.

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register/` | No | Register new user |
| POST | `/auth/token/` | No | Get JWT tokens |
| POST | `/auth/token/refresh/` | No | Refresh access token |
| GET | `/auth/me/` | Yes | Get current user |
| PUT | `/auth/me/` | Yes | Update profile |
| GET | `/auth/me/credits/` | Yes | Get credit balance |

### Skills Catalog

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/skills/` | No | List all skills |
| GET | `/skills/search/?q=python` | No | Search skills |
| POST | `/skills/` | Yes (Admin) | Create new skill |

### Teachable/Learnable Skills

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/skills/teachable/` | Yes | Skills I can teach |
| POST | `/skills/teachable/` | Yes | Add teachable skill |
| GET | `/skills/learnable/` | Yes | Skills I want to learn |
| POST | `/skills/learnable/` | Yes | Add learnable skill |

### Skill Exchange

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/exchanges/matches/` | Yes | Find exchange partners |
| GET | `/exchanges/proposals/` | Yes | List my proposals |
| POST | `/exchanges/proposals/` | Yes | Create proposal |
| PUT | `/exchanges/proposals/{id}/accept/` | Yes | Accept proposal |
| PUT | `/exchanges/proposals/{id}/complete/` | Yes | Complete exchange |

### Exchange Sessions

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/exchanges/sessions/` | Yes | List my sessions |
| POST | `/exchanges/sessions/` | Yes | Schedule session |
| PUT | `/exchanges/sessions/{id}/rate/` | Yes | Rate session |

### AI Recommendations

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/recommendations/career/` | Yes | Career path suggestions |
| GET | `/recommendations/skills/` | Yes | Skill gap analysis |
| GET | `/recommendations/roadmap/` | Yes | Learning roadmap |
| GET | `/recommendations/partners/` | Yes | Exchange partners |

### Skill Verification

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/verification/certificate/` | Yes | Upload certificate |
| GET | `/verification/certificates/` | Yes | List certificates |
| POST | `/verification/exam/start/` | Yes | Start exam |
| POST | `/verification/exam/submit/` | Yes | Submit exam |
| POST | `/verification/community/{user_id}/{skill_id}/` | Yes | Verify user's skill |
| GET | `/verification/status/{user_id}/` | No | View verification badges |

### Portfolio

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/portfolio/projects/` | Yes | List projects |
| POST | `/portfolio/projects/` | Yes | Add project |
| GET | `/portfolio/certifications/` | Yes | List certifications |
| POST | `/portfolio/certifications/` | Yes | Add certification |

### Full API Documentation

- **Swagger UI:** `http://localhost:8000/swagger/`
- **ReDoc:** `http://localhost:8000/redoc/`

---

## AI Recommendation Engine

Located in `apps/recommendations/recommendation_engine.py`

### Core Algorithms

| Module | Algorithm | Purpose |
|--------|-----------|---------|
| **Career Matching** | TF-IDF + Cosine Similarity | Match user skills to career paths |
| **Skill Gap Analysis** | Set Difference + Weighted Scoring | Identify missing skills |
| **Roadmap Generation** | Prerequisite Graph + Topological Sort | Ordered learning stages |
| **Partner Matching** | Collaborative Filtering | Find complementary skills |

### Career Matching Process

1. **Vectorization:** Convert user skills and career requirements into TF-IDF vectors
2. **Similarity Scoring:** Cosine similarity between user vector and career paths
3. **Boost Factors:** Interest alignment (+25%), industry demand (+15%), experience match (+10%)

### Skill Gap Analysis Response

```json
{
  "target_career": "Data Scientist",
  "match_score": 0.65,
  "matched_skills": ["Python", "SQL", "Statistics"],
  "missing_skills": [
    {"skill": "Machine Learning", "priority": "high", "estimated_hours": 40},
    {"skill": "TensorFlow", "priority": "medium", "estimated_hours": 30}
  ]
}
```

### Cache Strategy

- Career recommendations: **24 hours**
- Exchange partner matches: **1 hour**
- Manual refresh: `POST /api/recommendations/refresh/`

---

## Skill Exchange System

### Credit Economy

| Action | Credit Change |
|--------|---------------|
| Sign up | +5 beginner tokens |
| Teach 1 hour | +10 skill credits |
| Learn 1 hour | -10 skill credits |
| Refer a friend | +5 credits |
| Leave feedback | +1 credit |
| Verify another user | +2 credits |

### Pure Learner Support

Users with no teachable skills can still participate:

| Method | Description |
|--------|-------------|
| Beginner Tokens | 5 free on signup (1 token = 1 hour learning) |
| Referral Program | Invite friends to earn more tokens |
| Volunteer Tasks | Bug reporting, translation, moderation |
| Learn Then Teach | After 10 learning hours, qualify to teach basics |

### Exchange Flow

```
1. User adds Teachable Skills + Learnable Skills
2. AI finds matching users with complementary skills
3. User A sends ExchangeProposal to User B
4. User B accepts/rejects
5. Schedule sessions via ExchangeSession
6. Complete sessions and rate each other
7. Credits automatically transferred
```

---

## Skill Verification System

### Verification Levels

| Level | Badge | Requirement |
|-------|-------|-------------|
| 1 | 📝 Self-Declared | Add skill to profile |
| 2 | 👍 Community Verified | 3+ peer verifications |
| 3 | 🎓 Certificate Verified | Admin-approved certificate |
| 4 | ✅ Platform Tested | Pass on-site exam (80%+) |
| 5 | ⭐ Expert | Level 4 + 50+ hours + 4.8+ rating |

### Verification Methods

**1. Certificate Upload**
- Accepted sources: University degrees, MOOC platforms, Professional certs, Training centers
- Admin review within 48 hours

**2. On-Site Exam**
- Multiple choice and coding questions
- Auto-graded, 80% passing score
- 14-day retake cooldown if failed

**3. Community Verification**
- Learners verify teachers after successful sessions
- 3 verifications = Level 2

### Verification Rewards

| Achievement | Reward |
|-------------|--------|
| Level 2 | +10 credits + "Trusted" badge |
| Level 3 | +20 credits + "Certified" badge |
| Level 4 | +50 credits + Priority search |
| Level 5 | +100 credits + Featured status |

---

## Authentication

JWT via `djangorestframework-simplejwt`.

### Get Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Use Token

```bash
curl http://localhost:8000/api/skills/teachable/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..."
```

### Token Lifetimes

| Token | Lifetime | Configurable |
|-------|----------|--------------|
| Access | 1 hour | `JWT_ACCESS_TOKEN_LIFETIME` |
| Refresh | 24 hours | `JWT_REFRESH_TOKEN_LIFETIME` |

---

## Admin Panel

Django admin at `http://localhost:8000/admin/`

**Capabilities:**

- Manage users and credit balances
- Review certificate submissions
- Create skill assessment exams
- View platform analytics (exchanges, active users)
- Moderate skill categories
- Handle verification disputes
- Export usage reports

---

## Testing

```bash
# Run all tests
python manage.py test

# Test specific app
python manage.py test apps.exchanges
python manage.py test apps.recommendations
python manage.py test apps.verification

# With coverage
pip install coverage
coverage run manage.py test
coverage report
coverage html
```

**Target coverage:** 90%+ on exchanges, recommendations, and verification

---

## Deployment

### Deploy to Render (Free Tier)

**1.** Push code to GitHub

**2.** Create Web Service on Render:

| Setting | Value |
|---------|-------|
| Environment | Python |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| Start Command | `gunicorn skillbridge.wsgi:application` |

**3.** Add environment variables in Render dashboard

**4.** Add PostgreSQL add-on (free tier)

**5.** API live at: `https://your-app.onrender.com/api/`

### Production Checklist

- [ ] `DEBUG=False`
- [ ] Strong `SECRET_KEY`
- [ ] `ALLOWED_HOSTS` set to production domain
- [ ] PostgreSQL add-on attached
- [ ] CORS configured for frontend URL
- [ ] Email service configured
- [ ] Certificate storage (S3 or similar)

---

## Common Issues & Fixes

### PostgreSQL connection error

```bash
# Check if running
brew services list | grep postgresql  # macOS
sudo systemctl status postgresql      # Linux

# Start if stopped
brew services start postgresql@14
sudo systemctl start postgresql
```

### psycopg2 fails to install

```bash
# macOS
brew install postgresql
pip install psycopg2-binary

# Ubuntu
sudo apt install libpq-dev python3-dev
pip install psycopg2-binary
```

### Migration conflicts

```bash
# Development only — reset all migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

### CORS errors from frontend

```python
# settings.py
CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "https://your-frontend.vercel.app"]
CORS_ALLOW_CREDENTIALS = True
```

---

## Quick Reference

```bash
# Full reset (development only)
source venv/bin/activate
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Common commands
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test
python manage.py shell
python manage.py collectstatic
```

---

*SkillBridge — AI-Powered Skill Exchange Platform*
