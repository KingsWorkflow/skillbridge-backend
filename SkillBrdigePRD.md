# 📄 Product Requirements Document (PRD) – SkillBridge

## Skill Exchange Platform

**Version:** 1.0  
**Target Launch:** MVP in 2 weeks  
**Tech Stack:** Django 5.x, PostgreSQL, Django Templates, Alpine.js (minimal), Tailwind CSS (via CDN)  
**Authentication:** Django sessions (no DRF for pages, only for API endpoints)  

---

## 1. Executive Summary

SkillBridge is a **peer‑to‑peer skill exchange platform** where users can offer to teach skills they have and request to learn skills they want – **without any monetary transaction**. The platform uses a **skill credit economy** and a **verification system** (certificates, on‑site exams, community votes) to build trust. The MVP will be delivered as a server‑rendered Django application using pre‑designed HTML templates. The only dynamic parts will be a few lightweight API endpoints (e.g., for AI recommendations) and minimal Alpine.js for interactivity.

---

## 2. User Personas & Goals

| Persona | Goals | Pain Points Solved |
|---------|-------|---------------------|
| **Learner** (no skills to offer) | Learn a new skill for free | No money for courses; wants peer validation. |
| **Teacher** (has skills) | Share knowledge, earn skill credits, build reputation | Wants recognition and to learn other skills. |
| **Pure Learner** (teach nothing) | Still able to learn | Gets beginner tokens, can earn credits via referrals/volunteer. |
| **Admin** | Manage platform, verify certificates, moderate users | Ensure quality and trust. |

---

## 3. Functional Requirements

### 3.1 Authentication & User Management

| ID | Requirement |
|----|-------------|
| **AUTH-01** | Users can register with username, email, password, phone (optional), experience level (beginner/intermediate/advanced). |
| **AUTH-02** | After registration, user is automatically logged in and redirected to `/dashboard/`. |
| **AUTH-03** | Login via Django’s session‑based authentication (`LoginView`). |
| **AUTH-04** | Logout clears session, redirects to `/login/`. |
| **AUTH-05** | Profile page allows editing: bio, profile picture, phone, experience level. |
| **AUTH-06** | Password reset via email (console backend for MVP). |

### 3.2 Skill Management

| ID | Requirement |
|----|-------------|
| **SKL-01** | Admin can pre‑populate skills (e.g., Python, UI Design) via admin panel. |
| **SKL-02** | Users can add **teachable skills** (skill, proficiency level, weekly hours available). |
| **SKL-03** | Users can add **learnable skills** (skill, motivation text, urgency). |
| **SKL-04** | Users can edit/remove any of their own teachable/learnable skills. |
| **SKL-05** | Dashboard shows a summary of skills offered/wanted. |

### 3.3 Skill Exchange Proposals

| ID | Requirement |
|----|-------------|
| **EXP-01** | User A can send a proposal to User B: “I will teach you X if you teach me Y”. |
| **EXP-02** | Proposal includes proposed total hours (e.g., 10 hours), optional message. |
| **EXP-03** | User B can **accept**, **reject**, or **ignore** (leave pending). |
| **EXP-04** | Once accepted, both users can schedule **exchange sessions** (date, duration, meeting link). |
| **EXP-05** | After each session, both users can **rate** each other (1–5) and leave feedback. |
| **EXP-06** | After all sessions are marked completed, credits are automatically transferred (see section 4). |

### 3.4 Skill Credit Economy

| ID | Requirement |
|----|-------------|
| **ECO-01** | Every new user receives **5 beginner tokens** (can be used to learn without teaching). |
| **ECO-02** | Teaching 1 hour → earns **10 skill credits**. |
| **ECO-03** | Learning 1 hour → spends **10 skill credits** (or 1 beginner token if credits insufficient). |
| **ECO-04** | Credits can also be earned by: referring a friend (+5), leaving quality feedback (+1), reporting a bug (+2), volunteering (moderation, translation) (+10/week). |
| **ECO-05** | A transaction log records every credit change (type, amount, description, timestamp). |
| **ECO-06** | Users can view their credit balance and transaction history on the dashboard. |

### 3.5 AI Recommendations

| ID | Requirement |
|----|-------------|
| **AI-01** | On the `/exchange/` page, the system recommends potential exchange partners. |
| **AI-02** | Recommendations are based on **TF‑IDF + cosine similarity** between user’s teachable/learnable skills and others’ profiles. |
| **AI-03** | Each recommendation shows: mutual match score, which skills you would teach them, which you would learn. |
| **AI-04** | Recommendations are cached for 1 hour; manual refresh available. |

### 3.6 Skill Verification System

| ID | Requirement |
|----|-------------|
| **VER-01** | Each user‑skill pair can have a **verification level** (0‑5). |
| **VER-02** | **Level 1 – Self‑declared** (automatic when adding teachable skill). |
| **VER-03** | **Level 2 – Community verified** (after 3 distinct users verify that skill post‑exchange). |
| **VER-04** | **Level 3 – Certificate verified** (user uploads certificate; admin approves). |
| **VER-05** | **Level 4 – Platform tested** (user takes an on‑site exam; auto‑graded ≥80%). |
| **VER-06** | **Level 5 – Expert** (Level 4 + 50+ teaching hours + average rating ≥4.8). |
| **VER-07** | Verification badges are shown on profile and next to skills in search results. |
| **VER-08** | Verified teachers get priority in AI recommendations. |

### 3.7 Portfolio

| ID | Requirement |
|----|-------------|
| **POR-01** | Users can add **projects** (title, description, link, image). |
| **POR-02** | Users can add **certifications** (name, issuing org, date, certificate file). |
| **POR-03** | Portfolio is displayed on the user’s public profile. |

### 3.8 Admin Panel

| ID | Requirement |
|----|-------------|
| **ADM-01** | Admin can manage all users (view, disable, adjust credits). |
| **ADM-02** | Admin can approve/reject certificate uploads. |
| **ADM-03** | Admin can create/edit/delete skill exams (questions, passing score). |
| **ADM-04** | Admin can view platform analytics: total exchanges, active users, top skills, average ratings. |
| **ADM-05** | Admin can resolve disputes (e.g., cancel a proposal, adjust credits). |

---

## 4. Data Models (Django Models)

### 4.1 `users.UserProfile` (extends AbstractUser)

| Field | Type | Description |
|-------|------|-------------|
| `phone` | CharField(15) | optional |
| `profile_picture` | ImageField | upload to `profiles/` |
| `bio` | TextField(max_length=500) | optional |
| `experience_level` | CharField(20) | choices: `beginner`, `intermediate`, `advanced` |
| `skill_credits` | IntegerField | default 0 |
| `beginner_tokens` | IntegerField | default 5 |
| `reputation_score` | FloatField | average rating received (0‑5) |
| `total_hours_taught` | IntegerField | default 0 |
| `total_hours_learned` | IntegerField | default 0 |
| `created_at` | DateTimeField | auto_now_add |
| `updated_at` | DateTimeField | auto_now |

### 4.2 `skills.Skill`

| Field | Type |
|-------|------|
| `name` | CharField(100) unique |
| `category` | CharField(50) |
| `popularity_score` | FloatField(default=0) |

### 4.3 `skills.TeachableSkill`

| Field | Type | Constraints |
|-------|------|-------------|
| `user` | FK(UserProfile) | with `related_name='teachable_skills'` |
| `skill` | FK(Skill) | |
| `proficiency_level` | CharField(20) | `beginner`/`intermediate`/`expert` |
| `hourly_commitment` | IntegerField | hours/week available |
| `is_active` | BooleanField | default True |
| `created_at` | DateTimeField | auto_now_add |
| `class Meta` | unique_together | (`user`, `skill`) |

### 4.4 `skills.LearnableSkill`

| Field | Type |
|-------|------|
| `user` | FK(UserProfile, related_name='learnable_skills') |
| `skill` | FK(Skill) |
| `motivation` | TextField(blank=True) |
| `urgency` | CharField(10) | `low`/`medium`/`high` |
| `created_at` | DateTimeField |
| `Meta` | unique_together = (`user`, `skill`) |

### 4.5 `exchanges.ExchangeProposal`

| Field | Type | Choices |
|-------|------|---------|
| `proposer` | FK(UserProfile, related_name='sent_proposals') | |
| `receiver` | FK(UserProfile, related_name='received_proposals') | |
| `offer_skill` | FK(TeachableSkill) | |
| `request_skill` | FK(LearnableSkill) | |
| `proposed_hours` | IntegerField | |
| `message` | TextField(blank=True) | |
| `status` | CharField(20) | pending/accepted/rejected/completed/cancelled |
| `created_at` | DateTimeField | auto_now_add |
| `updated_at` | DateTimeField | auto_now |

### 4.6 `exchanges.ExchangeSession`

| Field | Type |
|-------|------|
| `proposal` | FK(ExchangeProposal, related_name='sessions') |
| `scheduled_date` | DateTimeField |
| `duration_hours` | IntegerField |
| `meeting_link` | URLField(blank=True) |
| `notes` | TextField(blank=True) |
| `teacher` | FK(UserProfile, related_name='teaching_sessions') |
| `learner` | FK(UserProfile, related_name='learning_sessions') |
| `skill_taught` | FK(Skill) |
| `completed` | BooleanField(default=False) |
| `teacher_rating` | IntegerField(null=True) | 1‑5 |
| `learner_rating` | IntegerField(null=True) | 1‑5 |
| `teacher_feedback` | TextField(blank=True) |
| `learner_feedback` | TextField(blank=True) |
| `created_at` | DateTimeField |

### 4.7 `exchanges.SkillCreditTransaction`

| Field | Type |
|-------|------|
| `user` | FK(UserProfile, related_name='transactions') |
| `amount` | IntegerField | (positive = earned, negative = spent) |
| `transaction_type` | CharField(30) | teach_earn/learn_spend/signup_bonus/referral_bonus/feedback_reward/verification_reward |
| `description` | TextField |
| `related_session` | FK(ExchangeSession, null=True, blank=True) |
| `created_at` | DateTimeField |

### 4.8 `verification.SkillVerification`

| Field | Type |
|-------|------|
| `user` | FK(UserProfile) |
| `skill` | FK(Skill) |
| `current_level` | IntegerField | 0‑5 |
| `self_declared_at` | DateTimeField | auto_now_add |
| `community_verified_at` | DateTimeField | null |
| `certificate_verified_at` | DateTimeField | null |
| `platform_tested_at` | DateTimeField | null |
| `expert_achieved_at` | DateTimeField | null |
| `verification_votes` | IntegerField | default 0 |
| `total_teaching_hours` | IntegerField | default 0 |
| `average_rating` | FloatField | default 0 |

### 4.9 `verification.Certificate`

| Field | Type |
|-------|------|
| `user` | FK(UserProfile) |
| `skill` | FK(Skill) |
| `certificate_file` | FileField | upload to `certificates/` |
| `issuing_organization` | CharField(200) |
| `certificate_id` | CharField(100, blank=True) |
| `issue_date` | DateField |
| `status` | CharField(20) | pending/approved/rejected |
| `rejection_reason` | TextField(blank=True) |
| `verified_by` | FK(UserProfile, null=True) |
| `verified_at` | DateTimeField(null=True) |

### 4.10 `verification.SkillExam`

| Field | Type |
|-------|------|
| `skill` | FK(Skill) |
| `difficulty` | CharField(20) | beginner/intermediate/advanced |
| `title` | CharField(200) |
| `time_limit_minutes` | IntegerField | default 30 |
| `passing_score` | IntegerField | default 70 |
| `questions` | JSONField | (list of question objects) |
| `is_active` | BooleanField | default True |
| `created_at` | DateTimeField |

### 4.11 `verification.ExamAttempt`

| Field | Type |
|-------|------|
| `user` | FK(UserProfile) |
| `exam` | FK(SkillExam) |
| `score` | FloatField |
| `passed` | BooleanField |
| `answers` | JSONField |
| `started_at` | DateTimeField | auto_now_add |
| `completed_at` | DateTimeField(null=True) |
| `can_retake_after` | DateTimeField(null=True) |

### 4.12 `portfolio.Project`

| Field | Type |
|-------|------|
| `user` | FK(UserProfile, related_name='projects') |
| `title` | CharField(200) |
| `description` | TextField |
| `project_url` | URLField(blank=True) |
| `image` | ImageField(upload_to='projects/', blank=True) |
| `created_at` | DateTimeField |

### 4.13 `portfolio.Certification`

| Field | Type |
|-------|------|
| `user` | FK(UserProfile, related_name='certifications') |
| `name` | CharField(200) |
| `issuing_organization` | CharField(200) |
| `issue_date` | DateField |
| `certificate_file` | FileField(upload_to='portfolio_certs/', blank=True) |
| `verification_url` | URLField(blank=True) |

---

## 5. URL Structure (Django URLs)

All URLs are prefixed with `/` (no `/api/` for pages; API endpoints are minimal and return JSON).

### 5.1 Public Pages
| URL | View | Template |
|-----|------|----------|
| `/` | `HomeView` | `core/index.html` |
| `/login/` | `LoginView` | `core/login.html` |
| `/register/` | `RegisterView` | `core/register.html` |
| `/logout/` | `LogoutView` | redirects |

### 5.2 Authenticated Pages
| URL | View | Template |
|-----|------|----------|
| `/dashboard/` | `DashboardView` | `core/dashboard.html` |
| `/profile/` | `ProfileView` | `core/profile.html` |
| `/skills/teachable/add/` | `AddTeachableSkillView` | (form snippet) |
| `/skills/learnable/add/` | `AddLearnableSkillView` | (form snippet) |
| `/exchange/` | `ExchangePartnersView` | `core/partners.html` |
| `/proposals/` | `ProposalsView` | `core/proposals.html` |
| `/proposals/create/` | `CreateProposalView` | JSON/redirect |
| `/proposals/<id>/accept/` | `AcceptProposalView` | redirect |
| `/sessions/schedule/` | `ScheduleSessionView` | form |
| `/sessions/<id>/rate/` | `RateSessionView` | form |
| `/verification/certificate/upload/` | `UploadCertificateView` | form |
| `/verification/exam/<skill_id>/start/` | `StartExamView` | template + JSON |
| `/portfolio/` | `PortfolioView` | `core/portfolio.html` |

### 5.3 API Endpoints (JSON, for AJAX/Alpine)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/recommendations/partners/` | Fetch AI partner matches (JSON) |
| POST | `/api/exchanges/proposals/` | Create proposal via fetch |
| GET | `/api/notifications/unread/` | Get pending notifications |
| POST | `/api/verification/community/<user_id>/<skill_id>/` | Verify a user’s skill |

All other interactions use standard Django forms and redirects.

---

## 6. User Flows

### 6.1 Registration & Onboarding
1. User clicks **Register**, fills form.
2. After submit, user is logged in → redirected to `/dashboard/`.
3. Dashboard shows beginner tokens and prompts to add skills.

### 6.2 Adding Skills to Teach
1. User goes to **Profile** → “Add Teachable Skill”.
2. Chooses skill from dropdown, proficiency, weekly hours.
3. Skill appears on profile; system automatically sets verification level to 1 (Self‑declared).

### 6.3 Finding Exchange Partners
1. User visits `/exchange/`.
2. AI recommendations load via AJAX (Alpine.js fetch).
3. For each partner, user sees which skills they would teach/learn.
4. User clicks “Propose Exchange” → form pre‑filled with skills.

### 6.4 Exchange Lifecycle
1. Proposer sends proposal → status = pending.
2. Receiver sees proposal on `/proposals/` and clicks Accept.
3. Both users can now schedule sessions (proposal detail page).
4. After each session, both users rate each other.
5. When all sessions are completed, the proposer (or receiver) clicks “Complete Exchange”.
6. System transfers credits and updates hours.

### 6.5 Skill Verification
- **Certificate**: User uploads PDF → admin approves → Level 3.
- **Community**: After a session, learner sees “Verify that teacher knows X” → click → teacher gets +1 vote. After 3 votes → Level 2.
- **Exam**: User starts exam → answers questions → auto‑graded → if ≥80% → Level 4.

---

## 7. Non‑Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Performance** | Page load < 2 seconds; AI recommendation response < 500 ms (cached). |
| **Security** | CSRF protection, session security, file upload validation. |
| **Scalability** | MVP: support up to 1000 concurrent users; PostgreSQL with proper indexes. |
| **Database** | Use `select_related` and `prefetch_related` to avoid N+1. |
| **Caching** | AI recommendations cached for 1 hour (Django cache framework). |
| **Mobile** | HTML templates must be responsive (Tailwind classes already present). |
| **Accessibility** | Basic WCAG 2.1 compliance (alt texts, keyboard navigation). |

---

## 8. Integration & External Services

| Service | Purpose | Notes |
|---------|---------|-------|
| **PostgreSQL** | Primary database | Use `psycopg2-binary`. |
| **Email (console)** | Password reset, notifications | `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` for MVP. |
| **File storage** | Profile pictures, certificates, portfolio images | Local `MEDIA_ROOT` (S3 optional post‑MVP). |
| **Alpine.js CDN** | Interactivity | `https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js` |
| **Axios** | AJAX | `https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js` |

---

## 9. Setup & Environment Variables (for Kilo Code)

### `.env` file (example)
```env
SECRET_KEY=django-insecure-xxxxxxxx
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=skillbridge_db
DB_USER=skillbridge_user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### `settings.py` must include:
```python
AUTH_USER_MODEL = 'users.UserProfile'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

## 10. Deliverables for Kilo Code

Kilo Code must generate the full Django project with:

- All models (as defined above) in their respective `models.py`.
- All admin registrations.
- All forms (custom registration, profile, teachable/learnable skills, exchange proposal, session rating, certificate upload).
- All views (class‑based or function) for every URL listed in section 5.
- All URL patterns.
- Templates: **do not rewrite the HTML**; assume they exist and use the following **context variable names**:

  - `dashboard.html`: expects `skill_credits`, `beginner_tokens`, `reputation_score`, `total_hours_taught`, `total_hours_learned`, `recent_proposals` (list).
  - `profile.html`: expects `form`, `teachable_skills`, `learnable_skills`, `all_skills`.
  - `partners.html`: expects `partners` (list of dicts with `partner_user`, `similarity_score`, `mutual_match_score`, `i_teach_they_learn`, `i_learn_they_teach`).
  - `proposals.html`: expects `sent_proposals`, `received_proposals`.
  - `portfolio.html`: expects `projects`, `certifications`.

- AI recommendation engine (`recommendation_engine.py`) with functions `build_user_feature_matrix()`, `find_exchange_partners(user_id, top_n=10)` using scikit‑learn.
- A simple API endpoint (JSON) at `/api/recommendations/partners/` that calls the engine.
- Unit tests for critical flows (registration, proposal creation, credit transfer).

---

## 11. Assumptions (no questions asked)

- The HTML templates from Google Stitch are already in `apps/core/templates/core/` and use Tailwind CSS CDN.
- No need to generate static CSS/JS files; only the backend logic.
- Kilo Code will produce a **single, runnable Django project** that can be cloned, migrated, and run immediately.
- The user (Prashanna) will run `python manage.py migrate`, `createsuperuser`, and `runserver`.

---

## 12. Success Criteria for MVP

- [ ] A new user can register, log in, and see their dashboard.
- [ ] User can add teachable and learnable skills.
- [ ] AI recommendations show potential exchange partners based on skills.
- [ ] User can send, accept, reject exchange proposals.
- [ ] Users can schedule sessions and rate after completion.
- [ ] Credits are transferred automatically.
- [ ] Admin can approve certificates and create exams.
- [ ] All pages are served from Django templates without frontend build step.

---

**End of PRD.** Kilo Code may now generate the entire project.