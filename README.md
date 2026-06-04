# SkillBridge  — Backend API

> AI-powered career guidance and skill exchange platform for students and young professionals.

**Stack:** Django 5.x · Django REST Framework · PostgreSQL 14+ · scikit-learn · JWT Auth  
**Deployed on:** Render (free tier)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Local Setup](#local-setup)
5. [Environment Variables](#environment-variables)
6. [Database Setup](#database-setup)
7. [Running the Server](#running-the-server)
8. [Project Structure](#project-structure)
9. [Database Models](#database-models)
10. [API Endpoints](#api-endpoints)
11. [AI Recommendation Engine](#ai-recommendation-engine)
12. [Authentication](#authentication)
13. [Admin Panel](#admin-panel)
14. [Testing](#testing)
15. [Deployment](#deployment)
16. [Common Issues & Fixes](#common-issues--fixes)
17. [Team Responsibilities](#team-responsibilities)
18. [Contributing Guidelines](#contributing-guidelines)

---

## Project Overview

SkillBridge  is a web-based platform where AI-guided career counselling meets a skill-sharing ecosystem. The backend exposes a RESTful API consumed by the React frontend.

**Core features this API powers:**

- JWT-based user registration and authentication
- AI-generated career recommendations using TF-IDF + Cosine Similarity
- Skill gap analysis comparing user skills to target careers
- Learning roadmap generation with ordered stages
- Peer-to-peer skill offering and session booking
- User portfolio management (projects + certifications)
- Admin panel for user management and platform analytics
- In-app and email notification system

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.10+ |
| Web Framework | Django | 5.x |
| REST API | Django REST Framework | 3.15+ |
| Database | PostgreSQL | 14+ |
| Auth | djangorestframework-simplejwt | latest |
| AI / ML | scikit-learn, pandas, numpy | latest |
| API Docs | drf-yasg (Swagger) | latest |
| CORS | django-cors-headers | latest |
| Environment | python-decouple | latest |
| Deployment | Render + Gunicorn | — |

---

## Prerequisites

Make sure the following are installed on your machine before setup:

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **PostgreSQL 14+** — [postgresql.org](https://www.postgresql.org/download/)
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

### 2. Create and activate a virtual environment

```bash
# Create
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
cp .env.example .env
```

Then edit `.env` with your local values (see [Environment Variables](#environment-variables) below).

### 5. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 7. (Optional) Load seed data

```bash
python manage.py loaddata fixtures/initial_data.json
```

### 8. Start the development server

```bash
python manage.py runserver
```

API is now live at: `http://localhost:8000/api/`  
Admin panel: `http://localhost:8000/admin/`  
Swagger docs: `http://localhost:8000/swagger/`

---

## Environment Variables

Create a `.env` file in the project root. **Never commit this file.**

```env
# Django
SECRET_KEY=your-super-secret-key-minimum-50-characters-long
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

# CORS (comma-separated frontend origins)
CORS_ALLOWED_ORIGINS=http://localhost:3000

# AI Engine (optional — Anthropic API key for enhanced recommendations)
ANTHROPIC_API_KEY=your-api-key-here

# Email (optional for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

See `.env.example` for a complete template with all supported variables.

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
python manage.py makemigrations users jobs applications recommendations
python manage.py migrate
```

### Reset migrations (development only)

```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

---

## Running the Server

```bash
# Development
python manage.py runserver

# Custom port
python manage.py runserver 8080

# Accessible on local network (for mobile testing)
python manage.py runserver 0.0.0.0:8000
```

---

## Project Structure

```
skillbridge-backend/
│
├── manage.py                    # Django management CLI
├── requirements.txt             # Python dependencies
├── .env                         # Local environment variables (git-ignored)
├── .env.example                 # Template for team members
├── .gitignore                   # Python / Django ignores
├── Procfile                     # Render/Heroku deployment command
│
├── skillbridge/                 # Project configuration package
│   ├── __init__.py
│   ├── settings.py              # All settings (reads from .env)
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI entry point (production)
│   └── asgi.py                  # ASGI entry point (async / websockets)
│
└── apps/                        # Django application modules
    │
    ├── users/                   # Custom user model + profiles
    │   ├── models.py            # UserProfile (extends AbstractUser)
    │   ├── serializers.py       # DRF serializers
    │   ├── views.py             # Registration, login, profile CRUD
    │   ├── urls.py              # /api/auth/* routes
    │   ├── admin.py             # Admin panel registration
    │   └── tests.py             # Unit + integration tests
    │
    ├── jobs/                    # Job listings, skills, companies
    │   ├── models.py            # Job, Skill, Company
    │   ├── serializers.py
    │   ├── views.py             # Job CRUD + search/filter
    │   ├── urls.py              # /api/jobs/* routes
    │   ├── admin.py
    │   └── tests.py
    │
    ├── applications/            # Job application workflow
    │   ├── models.py            # Application (user → job)
    │   ├── serializers.py
    │   ├── views.py             # Apply, track status
    │   ├── urls.py              # /api/applications/* routes
    │   ├── admin.py
    │   └── tests.py
    │
    └── recommendations/         # AI engine
        ├── models.py            # Cached recommendation results
        ├── recommendation_engine.py   # Core TF-IDF + cosine similarity
        ├── skill_vectorizer.py        # Skill → vector transformation
        ├── views.py             # /api/recommendations/* endpoints
        ├── urls.py
        └── tests.py
```

---

## Database Models

### UserProfile (extends AbstractUser)

| Field | Type | Description |
|---|---|---|
| `username` | CharField | Unique login handle |
| `email` | EmailField | Unique email address |
| `phone` | CharField | Optional phone number |
| `address` | TextField | Location|
| `profile_picture` | ImageField | Avatar upload |
| `experience_level` | CharField | `entry` / `mid` / `senior` |
| `skills` | ManyToManyField | → Skill model |

### Job

| Field | Type | Description |
|---|---|---|
| `title` | CharField | Job title |
| `description` | TextField | Full job description |
| `requirements` | TextField | Required qualifications |
| `job_type` | CharField | `full-time` / `part-time` / `contract` / `internship` |
| `location` | CharField | City or Remote |
| `salary_min` | DecimalField | Minimum salary (NPR) |
| `salary_max` | DecimalField | Maximum salary (NPR) |
| `deadline` | DateField | Application deadline |
| `is_active` | BooleanField | Visibility toggle |
| `company` | ForeignKey | → Company |
| `required_skills` | ManyToManyField | → Skill |

### Skill

| Field | Type | Description |
|---|---|---|
| `name` | CharField | Skill name e.g. "Django" |
| `category` | CharField | e.g. "Backend", "Frontend", "AI/ML" |

### Application

| Field | Type | Description |
|---|---|---|
| `applicant` | ForeignKey | → User |
| `job` | ForeignKey | → Job |
| `cover_letter` | TextField | Applicant's cover letter |
| `resume` | FileField | Uploaded resume (PDF) |
| `portfolio_url` | URLField | Optional portfolio link |
| `status` | CharField | `pending` / `reviewed` / `shortlisted` / `rejected` / `hired` |
| `applied_at` | DateTimeField | Auto timestamp |

---

## API Endpoints

All endpoints are prefixed with `/api/`.

### Authentication

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| POST | `/auth/register/` | No | Register new user |
| POST | `/auth/token/` | No | Obtain JWT access + refresh tokens |
| POST | `/auth/token/refresh/` | No | Refresh expired access token |
| GET | `/auth/me/` | Yes | Get current user profile |
| PUT | `/auth/me/` | Yes | Update profile |
| POST | `/auth/logout/` | Yes | Blacklist refresh token |

### Jobs

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/jobs/` | No | List all active jobs (paginated) |
| POST | `/jobs/` | Yes (Admin) | Create new job listing |
| GET | `/jobs/{id}/` | No | Get job detail |
| PUT | `/jobs/{id}/` | Yes (Admin) | Update job |
| DELETE | `/jobs/{id}/` | Yes (Admin) | Delete job |
| GET | `/jobs/?search=python` | No | Search jobs by keyword |
| GET | `/jobs/?skill=django&type=full-time` | No | Filter by skill and type |

### Applications

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/applications/` | Yes | List my applications |
| POST | `/applications/` | Yes | Apply for a job |
| GET | `/applications/{id}/` | Yes | Get application detail |
| PATCH | `/applications/{id}/status/` | Yes (Admin) | Update application status |

### Recommendations

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/recommendations/` | Yes | Get AI job recommendations |
| POST | `/recommendations/refresh/` | Yes | Force regenerate recommendations |

### Skills

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/skills/` | No | List all skills |
| POST | `/skills/` | Yes (Admin) | Create skill |

### Full API documentation (Swagger UI): `http://localhost:8000/swagger/`  
### ReDoc: `http://localhost:8000/redoc/`

---

## AI Recommendation Engine

Located in `apps/recommendations/recommendation_engine.py`.

### Algorithm

1. **TF-IDF Vectorization** — converts user skill list and job requirement text into numerical vectors
2. **Cosine Similarity** — measures how closely a user's skills match each job's requirements
3. **Boost Factors** applied on top of similarity score:

| Factor | Adjustment |
|---|---|
| Experience level exact match | +30% |
| One level off (Senior → Mid) | +10% |
| Job already applied to | −50% |

### Cache Strategy

- Recommendations are cached for **1 hour** per user using Django's cache framework
- Cache key: `recommendations_user_{user_id}`
- Manual refresh available via `POST /api/recommendations/refresh/`

### Key files

```
apps/recommendations/
├── recommendation_engine.py   # Core matching logic
├── skill_vectorizer.py        # Skill list → TF-IDF vector
└── views.py                   # API endpoints + cache logic
```

---

## Authentication

This project uses **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`.

### How to authenticate API requests

```bash
# 1. Obtain tokens
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Response
{
  "access": "eyJ0eXAiOiJKV1Qi...",
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}

# 2. Use access token in subsequent requests
curl http://localhost:8000/api/jobs/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..."

# 3. Refresh expired access token
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -d '{"refresh": "eyJ0eXAiOiJKV1Qi..."}'
```

**Token lifetimes** (configurable in `.env`):

- Access token: `1 hour` (3600 seconds)
- Refresh token: `24 hours` (86400 seconds)

---

## Admin Panel

Django's built-in admin is available at `http://localhost:8000/admin/`.

Log in with the superuser credentials you created during setup.

**What admins can do:**

- Manage all users and their profiles
- Create, edit, and deactivate job listings
- Review and update application statuses
- View platform analytics reports
- Configure AI engine API keys
- Monitor skill offerings and sessions

---

## Testing

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test apps.users
python manage.py test apps.recommendations

# Run with verbosity
python manage.py test --verbosity=2

# Run with pytest (if installed)
pytest

# Check test coverage
pip install coverage
coverage run manage.py test
coverage report
coverage html   # Open htmlcov/index.html in browser
```

**Target:** 90%+ coverage on critical paths (auth, recommendations, applications).

---

## Deployment

### Deploy to Render (free tier)

**1. Push your code to GitHub.**

**2. Create a new Web Service on [render.com](https://render.com):**

- Environment: `Python`
- Build command:
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- Start command:
  ```bash
  gunicorn skillbridge.wsgi:application
  ```

**3. Add environment variables** in Render dashboard (same as `.env` but with production values):

```
SECRET_KEY=<strong-production-key>
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=<auto-filled by Render PostgreSQL add-on>
```

**4. Add PostgreSQL add-on** in Render dashboard (free tier available).

**5. Your API will be live at:** `https://your-app.onrender.com/api/`

### Production checklist

- [ ] `DEBUG=False` in environment
- [ ] Strong `SECRET_KEY` (50+ random characters)
- [ ] `ALLOWED_HOSTS` set to production domain
- [ ] `collectstatic` runs in build command
- [ ] PostgreSQL add-on attached
- [ ] All environment variables set in dashboard
- [ ] CORS configured for frontend production URL

---

## Common Issues & Fixes

### PostgreSQL connection error

```bash
# Check if PostgreSQL is running
# macOS
brew services list | grep postgresql

# Linux
sudo systemctl status postgresql

# Start if stopped
brew services start postgresql@14   # macOS
sudo systemctl start postgresql      # Linux
```

### psycopg2 installation fails

```bash
# macOS
brew install postgresql
pip install psycopg2-binary

# Ubuntu / Debian
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
# settings.py — add your frontend origin
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend.vercel.app",
]
CORS_ALLOW_CREDENTIALS = True
```

### ModuleNotFoundError after installing package

```bash
# Make sure your venv is activated
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

---

## Team Responsibilities

| Member | Role | Primary Files |
|---|---|---|
| **Dev 1** | Backend + AI/ML | `apps/recommendations/`, `apps/jobs/models.py`, PostgreSQL schema |
| **Dev 2** | Backend + Auth | `apps/users/`, `skillbridge/settings.py`, JWT config, `apps/*/admin.py` |
| **Dev 3** | Frontend UI | (see frontend repo) |
| **Dev 4** | Frontend Integration | (see frontend repo) |

---

## Contributing Guidelines

1. **Never commit `.env`** — it is in `.gitignore` for a reason
2. **Always work in a feature branch** — never push directly to `main`
3. **Run migrations after every model change** — `python manage.py makemigrations && python manage.py migrate`
4. **Write tests for every new view** — aim for 90%+ coverage
5. **Use `select_related` / `prefetch_related`** to avoid N+1 query problems
6. **Coordinate API contracts** with Dev 3 and Dev 4 before changing endpoint signatures
7. **Use PostgreSQL** throughout development — never SQLite
8. **Cache AI recommendations** — never recompute on every request

### Branch naming convention

```
feature/add-skill-gap-analysis
fix/jwt-token-refresh-bug
chore/update-requirements
```

### Pull request checklist

- [ ] Tests pass locally (`python manage.py test`)
- [ ] No new migration conflicts
- [ ] `.env` not committed
- [ ] API changes communicated to frontend team
- [ ] Code reviewed by at least one other team member

---

## Quick Reference

```bash
# Full reset and start fresh (dev only)
source venv/bin/activate
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Common commands
python manage.py makemigrations       # Generate migration files
python manage.py migrate              # Apply migrations to DB
python manage.py createsuperuser      # Create admin user
python manage.py runserver            # Start dev server
python manage.py test                 # Run all tests
python manage.py shell                # Django interactive shell
python manage.py collectstatic        # Gather static files (production)
```

---

*SkillBridge  — Built by Team of 4 | 2-Week Sprint | Westcliff University / King's College Kathmandu*