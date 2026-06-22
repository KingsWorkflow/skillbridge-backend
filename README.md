# SkillBridge — Peer-to-Peer Skill Exchange Platform

> A Django-based skill exchange platform where users teach skills they have and learn skills they want — **without any monetary transaction**.  
> *Peer-to-peer skill sharing · Skill credit economy · Verified teaching · Free for everyone*

**Stack:** Django 5.x · PostgreSQL 14+ · Django Templates · Tailwind CSS (CDN) · Alpine.js (minimal)

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
12. [Frontend Pages](#frontend-pages)
13. [API Endpoints](#api-endpoints)
14. [Skill Matching Engine](#skill-matching-engine)
15. [Skill Exchange System](#skill-exchange-system)
16. [Skill Verification System](#skill-verification-system)
17. [Authentication](#authentication)
18. [Admin Panel](#admin-panel)
19. [Testing](#testing)
20. [Deployment](#deployment)
21. [Common Issues & Fixes](#common-issues--fixes)

---

## Project Overview

**SkillBridge** is a server-rendered Django application for peer-to-peer skill exchange. Users offer to teach skills they have and request to learn skills they want — no money involved. The platform uses a **skill credit economy** and a **simplified 3-level verification system** (self-declared, community rated, platform tested) to build trust.

### Core Features

| Feature | Description |
|---------|-------------|
| **Session Authentication** | Django session-based login (no JWT for pages) |
| **Skill Management** | Add teachable and learnable skills with proficiency, hours, and urgency |
| **Skill Matching** | Simple keyword/string matching (no AI/ML) to find exchange partners |
| **Exchange Proposals** | Send, accept, reject skill exchange requests with optional messages |
| **Session Scheduling** | Schedule exchange sessions with date, duration, and meeting link |
| **Session Ratings** | Rate each other 1–5 after session completion |
| **Skill Credit Economy** | Earn/spend credits for teaching/learning; beginner tokens for new users |
| **Skill Verification** | 3-level verification: self-declared, community rated, platform tested |
| **On-site Exams** | Admin-created exams with weighted objective/subjective questions, auto-grading |
| **Portfolio** | Showcase projects and auto-generated exam certificates |
| **Admin Panel** | User management, exam creation, certificate approval, analytics, bulk verify |
| **Notifications** | In-app notifications for proposals and exchanges |

### Platform Philosophy

> *"Everyone has something to teach. Everyone has something to learn. No money required."*

- **Pure learners** (no skills to offer) earn credits through referrals, feedback, or community contributions
- **Skill credits** system ensures fair exchange without currency
- **Beginner tokens** (5 free on signup) let anyone start learning immediately
- **Verification badges** (3 levels) build trust in skill claims

---

## Problem Statement

The major issues that motivated this project are:

| Problem | Description |
|---------|-------------|
| **Skills-Industry Gap** | Graduates often lack skills required by the job market, resulting in high unemployment or underemployment |
| **Lack of Accessible Learning** | Expensive courses and training programs are inaccessible to many |
| **Poor Peer Learning Infrastructure** | No formal structure to share skills and encourage collaborative learning |
| **Information Asymmetry** | Students lack access to current information about in-demand skills and industry trends |
| **Limited Portfolio Tools** | Students lack tools to create professional portfolios showcasing projects and certifications |
| **Trust Deficit** | Hard to verify claimed skills without expensive third-party certification |

These issues limit professional development and decrease human capital productivity. SkillBridge directly addresses these problem dimensions through an integrated digital platform.

---

## Objectives

### Main Objective

To provide a web-based skill exchange platform that enables students and young professionals to teach and learn skills from peers — all without monetary transactions.

### Specific Objectives

| # | Objective |
|---|-----------|
| 1 | Enable users to register, log in, and manage their profile securely |
| 2 | Allow users to add teachable skills (skill, proficiency, weekly hours) |
| 3 | Allow users to add learnable skills (skill, motivation, urgency) |
| 4 | Match users with complementary skills using simple keyword matching |
| 5 | Enable skill exchange proposals with accept/reject workflow |
| 6 | Schedule and rate exchange sessions |
| 7 | Transfer skill credits automatically after completed sessions |
| 8 | Build a 3-level skill verification system (self-declared, community rated, platform tested) |
| 9 | Provide admin tools for exam creation, certificate approval, and analytics |
| 10 | Help users build professional portfolios with projects and verified certifications |

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.10+ |
| Web Framework | Django | 5.x |
| Database | PostgreSQL | 14+ |
| Frontend | Django Templates + Tailwind CSS (CDN) + Alpine.js | — |
| Authentication | Django sessions | — |
| Admin | Django Admin + custom overrides | — |
| File Storage | Local MEDIA_ROOT | — |

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
| App | `http://localhost:8000/` |
| Admin Panel | `http://localhost:8000/admin/` |

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

# Auth
LOGIN_URL=/login/
LOGIN_REDIRECT_URL=/dashboard/
LOGOUT_REDIRECT_URL=/login/

# Skill Exchange System
DEFAULT_BEGINNER_TOKENS=5
SKILL_CREDIT_EARN_RATE=10
SKILL_CREDIT_SPEND_RATE=10

# Verification System
COMMUNITY_VERIFICATION_THRESHOLD=3
EXAM_PASSING_SCORE=80
EXAM_RETAKE_COOLDOWN_DAYS=30

# Email (optional for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
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
python manage.py makemigrations users skills exchanges recommendations verification portfolio notifications
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
│
├── skillbridge/                 # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/                      # Global static files
│   ├── admin/css/               # Admin CSS overrides
│   └── verification/            # Verification app static
│
├── templates/                   # Global templates
│   ├── base.html
│   ├── admin/                   # Admin templates
│   └── ...                      # App-specific templates
│
└── apps/
    ├── users/                   # User profiles, auth, dashboard
    ├── skills/                  # Skill catalog, teachable/learnable skills
    ├── exchanges/               # Proposals, sessions, credit transactions
    ├── recommendations/         # Keyword-based partner matching
    ├── verification/            # Skill verification, exams, certificates
    ├── portfolio/               # Projects and certifications
    ├── notifications/           # In-app notifications
    ├── admin_custom/            # Custom admin views (analytics, bulk verify)
    └── careers/                 # Career-related pages
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
| `teacher_feedback` | TextField | Optional feedback |
| `learner_feedback` | TextField | Optional feedback |

### SkillCreditTransaction

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | → UserProfile |
| `amount` | IntegerField | Positive = earned, Negative = spent |
| `transaction_type` | CharField | `teach_earn` / `learn_spend` / `signup_bonus` / `referral_bonus` / `feedback_reward` / `verification_reward` |
| `description` | TextField | Transaction details |
| `related_session` | ForeignKey | → ExchangeSession (nullable) |

### SkillVerification (3 Levels)

| Level | Badge | Meaning | Requirement |
|-------|-------|---------|-------------|
| 1 | Self-declared | User claims the skill | Automatic when adding teachable skill |
| 2 | Community rated | Peer-validated | ≥3 session ratings with average ≥4.0 |
| 3 | Platform tested | Exam verified | Pass on-site exam (≥80%) + admin approval |

### Certificate

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | → UserProfile |
| `skill` | ForeignKey | → Skill |
| `certificate_file` | FileField | Uploaded PDF/image |
| `issuing_organization` | CharField | e.g., "Coursera", "SkillBridge Nepal" |
| `issue_date` | DateField | Date of certification |
| `status` | CharField | `pending` / `approved` / `rejected` |
| `verified_by` | ForeignKey | → UserProfile (admin) |
| `verified_at` | DateTimeField | When approved/rejected |

### SkillExam

| Field | Type | Description |
|-------|------|-------------|
| `skill` | ForeignKey | → Skill |
| `difficulty` | CharField | `beginner` / `intermediate` / `advanced` |
| `title` | CharField | Exam title |
| `time_limit_minutes` | IntegerField | Default 30 |
| `passing_score` | IntegerField | Default 70 |
| `is_active` | BooleanField | Default True |
| `created_at` | DateTimeField | Auto-set |

### Question

| Field | Type | Description |
|-------|------|-------------|
| `exam` | ForeignKey | → SkillExam |
| `text` | TextField | Question text |
| `question_type` | CharField | `objective` / `subjective` |
| `options` | JSONField | List of options for objective questions |
| `correct_index` | IntegerField | 0-based index of correct answer |
| `model_answer` | TextField | Expected answer for subjective questions |
| `weight` | IntegerField | Marks for this question |
| `explanation` | TextField | Explanation shown after answering |
| `order` | IntegerField | Display order |

### ExamAttempt

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | → UserProfile |
| `exam` | ForeignKey | → SkillExam |
| `score` | FloatField | Percentage score |
| `passed` | BooleanField | Met passing score? |
| `answers` | JSONField | Submitted answers |
| `started_at` | DateTimeField | Auto-set |
| `completed_at` | DateTimeField |null |
| `can_retake_after` | DateTimeField | 30-day cooldown if failed |

---

## Frontend Pages

All pages are server-rendered Django templates with Tailwind CSS (CDN) and minimal Alpine.js.

| URL | View | Template | Description |
|-----|------|----------|-------------|
| `/` | `HomeView` | `core/index.html` | Landing page |
| `/login/` | `LoginView` | `core/login.html` | Session-based login |
| `/register/` | `RegisterView` | `core/register.html` | User registration |
| `/logout/` | `LogoutView` | redirects | Clears session |
| `/dashboard/` | `DashboardView` | `core/dashboard.html` | User dashboard |
| `/profile/` | `ProfileView` | `core/profile.html` | Edit profile |
| `/skills/teachable/` | `TeachableSkillsView` | `skills/teachable_skills.html` | Add/manage teachable skills |
| `/skills/learnable/` | `LearnableSkillsView` | `skills/learnable_skills.html` | Add/manage learnable skills |
| `/skills/catalog/` | `SkillListView` | `skills/skill_list.html` | Browse all skills |
| `/exchange/` | `ExchangePartnersView` | `core/partners.html` | Find exchange partners |
| `/proposals/` | `ProposalsView` | `core/proposals.html` | Sent/received proposals |
| `/sessions/` | `SessionListView` | `exchanges/session_list.html` | Upcoming sessions |
| `/verification/status/` | `VerificationStatusView` | `verification/verification_status.html` | Verification levels |
| `/verification/exam/<skill_id>/start/` | `StartExamView` | `verification/exam_start.html` | Take exam |
| `/verification/exam/submit/` | `ExamSubmitView` | `verification/exam_submit.html` | Exam result |
| `/verification/certificates/` | `CertificateListView` | `verification/certificate_list.html` | Approved certificates |
| `/portfolio/` | `PortfolioView` | `portfolio/portfolio.html` | Projects + verified skills |
| `/careers/` | `CareerView` | `careers/career_list.html` | Career listings |
| `/notifications/` | `NotificationListView` | `notifications/notification_list.html` | In-app notifications |

---

## API Endpoints

All API endpoints return JSON and are used for AJAX/Alpine.js interactions.

### Verification API

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/verification/status/` | Yes | Current user's verification matrix |
| GET | `/api/verification/exams/` | Yes | List active exams (optional `?skill_id=`) |
| GET | `/api/verification/exams/<exam_id>/` | Yes | Single exam detail with questions |
| POST | `/api/verification/exams/<exam_id>/submit/` | Yes | Submit answers, auto-grade, record attempt |
| POST | `/api/verification/community/verify/<user_id>/<skill_id>/` | Yes | Cast community vote |

### Recommendation API (Keyword Matching)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/match/partners/` | Yes | Fetch skill-matched partners (simple keyword matching) |

### Notifications API

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/notifications/unread/` | Yes | Get pending notifications |

---

## Skill Matching Engine

Located in `apps/recommendations/engine.py`

### Approach

**No AI/ML is used.** Matching is based on simple keyword/string matching (case-insensitive) between users' teachable and learnable skills.

### Algorithm

1. Build an index of all users' teachable and learnable skills
2. For the current user, find other users whose teachable skills match the current user's learnable skills (and vice versa)
3. Score matches by number of overlapping skill keywords
4. Return top-N partners with similarity scores and skill match details

### Caching

- Partner matches are cached for **1 hour**
- Manual refresh available via browser reload

---

## Skill Exchange System

### Credit Economy

| Action | Credit Change |
|--------|---------------|
| Sign up | +5 beginner tokens |
| Teach 1 hour | +10 skill credits |
| Learn 1 hour | -10 skill credits (or 1 beginner token) |
| Refer a friend | +5 credits |
| Leave quality feedback | +1 credit |
| Report a bug | +2 credits |

### Transaction Log

Every credit change is recorded in `SkillCreditTransaction` with:
- `amount` (positive = earned, negative = spent)
- `transaction_type` (teach_earn, learn_spend, signup_bonus, referral_bonus, feedback_reward, verification_reward)
- `description`
- `created_at`

### Exchange Flow

```
1. User adds Teachable Skills + Learnable Skills
2. Keyword matching finds complementary partners
3. User A sends ExchangeProposal to User B
4. User B accepts/rejects/ignores
5. Both users schedule ExchangeSessions
6. After each session, both rate each other (1-5)
7. When all sessions completed, credits auto-transfer
```

### Proposal Lifecycle

| Status | Meaning |
|--------|---------|
| `pending` | Awaiting response |
| `accepted` | Both users agreed |
| `rejected` | Receiver declined |
| `completed` | All sessions done, credits transferred |
| `cancelled` | Proposal cancelled by either party |

---

## Skill Verification System

### 3-Level Verification

| Level | Name | How to Achieve |
|-------|------|----------------|
| 1 | Self-declared | Automatic when user adds a teachable skill |
| 2 | Community rated | Skill receives ≥3 session ratings with average ≥4.0 from unique learners |
| 3 | Platform tested | User passes admin-created on-site exam (≥80%) |

### On-Site Exams

- Admin creates exams via Django admin with `Question` inlines
- Questions can be **objective** (multiple choice) or **subjective** (text answer)
- Each question has a **weight** (marks) and optional **explanation**
- Exams are auto-graded on submit:
  - Objective: compare selected option index to `correct_index`
  - Score = `(earned_marks / total_weight) × 100`
- Passing: `score ≥ passing_score` (default 70%)
- Failed attempts: 30-day retake cooldown (`can_retake_after`)
- Admin reviews attempts in `ExamAttemptAdmin` and can set `passed=True`

### Certificate Auto-Generation

When an `ExamAttempt` is marked `passed=True`, a `Certificate` record is automatically created with:
- `issuing_organization = 'SkillBridge Nepal'`
- `status = 'approved'`
- `issue_date = today`
- Appears on user's portfolio under "Verified Skills"

---

## Authentication

**Session-based authentication** using Django's built-in `LoginView` / `LogoutView`.

- No JWT for page views
- No DRF for standard pages
- API endpoints use `@login_required` with session cookies
- Password reset via console email backend (MVP)

---

## Admin Panel

Django admin at `http://localhost:8000/admin/`

### Custom Admin Features

- **SkillExam Admin** — create/edit exams with inline `Question` editor (objective + subjective, weighted scoring)
- **Certificate Admin** — approve/reject certificates with bulk actions
- **ExamAttempt Admin** — review exam results, mark passed/failed
- **Analytics Dashboard** — `/admin/analytics/` with platform stats
- **Bulk Verify** — `/admin/bulk-verify/` for CSV-based certificate approval
- **Custom CSS** — scoped admin redesign under `body.django-admin-override`

### Admin URL Structure

| URL | View | Description |
|-----|------|-------------|
| `/admin/` | Django admin | Standard model management |
| `/admin/analytics/` | `analytics_dashboard` | Platform analytics |
| `/admin/bulk-verify/` | `bulk_verify_view` | Bulk certificate verification |

---

## Testing

```bash
# Run all tests
python manage.py test

# Test specific app
python manage.py test apps.exchanges
python manage.py test apps.verification
python manage.py test apps.skills

# With coverage
pip install coverage
coverage run manage.py test
coverage report
coverage html
```

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

**5.** App live at: `https://your-app.onrender.com/`

### Production Checklist

- [ ] `DEBUG=False`
- [ ] Strong `SECRET_KEY`
- [ ] `ALLOWED_HOSTS` set to production domain
- [ ] PostgreSQL add-on attached
- [ ] Email service configured (optional)
- [ ] Media files configured (S3 or similar for production)

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

### Static files not loading

```bash
python manage.py collectstatic --noinput
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

*SkillBridge — Peer-to-Peer Skill Exchange Platform*
