-- SkillBridge Database Schema (PostgreSQL)
-- Based on PRD Section 4: Data Models
-- Usage: psql -U <user> -d <dbname> -f skillbridge_schema.sql

-- Drop existing tables (optional, for clean setup)
-- DROP TABLE IF EXISTS portfolio_certification, portfolio_project, verification_examattempt,
-- verification_skillexam, verification_certificate, verification_skillverification,
-- exchanges_skillcredittransaction, exchanges_exchangesession, exchanges_exchangeproposal,
-- skills_learnableskill, skills_teachableskill, skills_skill, users_userprofile CASCADE;

-- 4.1 users.UserProfile (extends AbstractUser)
CREATE TABLE users_userprofile (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    phone VARCHAR(15) NULL,
    profile_picture VARCHAR(100) NULL,
    bio TEXT NULL,
    experience_level VARCHAR(20) NOT NULL DEFAULT 'beginner' CHECK (experience_level IN ('beginner', 'intermediate', 'advanced')),
    skill_credits INTEGER NOT NULL DEFAULT 0,
    beginner_tokens INTEGER NOT NULL DEFAULT 5,
    reputation_score FLOAT NULL,
    total_hours_taught INTEGER NOT NULL DEFAULT 0,
    total_hours_learned INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- 4.2 skills.Skill
CREATE TABLE skills_skill (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,
    popularity_score FLOAT NOT NULL DEFAULT 0
);

-- 4.3 skills.TeachableSkill
CREATE TABLE skills_teachableskill (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills_skill(id) ON DELETE CASCADE,
    proficiency_level VARCHAR(20) NOT NULL CHECK (proficiency_level IN ('beginner', 'intermediate', 'expert')),
    hourly_commitment INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, skill_id)
);

-- 4.4 skills.LearnableSkill
CREATE TABLE skills_learnableskill (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills_skill(id) ON DELETE CASCADE,
    motivation TEXT NULL,
    urgency VARCHAR(10) NOT NULL CHECK (urgency IN ('low', 'medium', 'high')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, skill_id)
);

-- 4.5 exchanges.ExchangeProposal
CREATE TABLE exchanges_exchangeproposal (
    id SERIAL PRIMARY KEY,
    proposer_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    receiver_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    offer_skill_id INTEGER NOT NULL REFERENCES skills_teachableskill(id) ON DELETE CASCADE,
    request_skill_id INTEGER NOT NULL REFERENCES skills_learnableskill(id) ON DELETE CASCADE,
    proposed_hours INTEGER NOT NULL,
    message TEXT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected', 'completed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- 4.6 exchanges.ExchangeSession
CREATE TABLE exchanges_exchangesession (
    id SERIAL PRIMARY KEY,
    proposal_id INTEGER NOT NULL REFERENCES exchanges_exchangeproposal(id) ON DELETE CASCADE,
    scheduled_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_hours INTEGER NOT NULL,
    meeting_link VARCHAR(200) NULL,
    notes TEXT NULL,
    teacher_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    learner_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    skill_taught_id INTEGER NOT NULL REFERENCES skills_skill(id) ON DELETE CASCADE,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    teacher_rating INTEGER NULL CHECK (teacher_rating BETWEEN 1 AND 5),
    learner_rating INTEGER NULL CHECK (learner_rating BETWEEN 1 AND 5),
    teacher_feedback TEXT NULL,
    learner_feedback TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- 4.7 exchanges.SkillCreditTransaction
CREATE TABLE exchanges_skillcredittransaction (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    transaction_type VARCHAR(30) NOT NULL CHECK (transaction_type IN ('teach_earn', 'learn_spend', 'signup_bonus', 'referral_bonus', 'feedback_reward', 'verification_reward')),
    description TEXT NOT NULL,
    related_session_id INTEGER NULL REFERENCES exchanges_exchangesession(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- 4.8 verification.SkillVerification
-- Note: average_rating is a generated column (requires PostgreSQL 12+)
CREATE TABLE verification_skillverification (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills_skill(id) ON DELETE CASCADE,
    current_level INTEGER NOT NULL DEFAULT 1 CHECK (current_level BETWEEN 1 AND 3),
    self_declared_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    community_rated_at TIMESTAMP WITH TIME ZONE NULL,
    platform_tested_at TIMESTAMP WITH TIME ZONE NULL,
    rating_sum FLOAT NOT NULL DEFAULT 0,
    rating_count INTEGER NOT NULL DEFAULT 0,
    average_rating FLOAT GENERATED ALWAYS AS (CASE WHEN rating_count = 0 THEN 0 ELSE rating_sum / rating_count END) STORED,
    UNIQUE(user_id, skill_id)
);

-- 4.9 verification.Certificate
CREATE TABLE verification_certificate (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills_skill(id) ON DELETE CASCADE,
    certificate_file VARCHAR(100) NULL,
    issuing_organization VARCHAR(200) NOT NULL,
    certificate_id VARCHAR(100) NULL,
    issue_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    rejection_reason TEXT NULL,
    verified_by_id INTEGER NULL REFERENCES users_userprofile(id) ON DELETE SET NULL,
    verified_at TIMESTAMP WITH TIME ZONE NULL
);

-- 4.10 verification.SkillExam
CREATE TABLE verification_skillexam (
    id SERIAL PRIMARY KEY,
    skill_id INTEGER NOT NULL REFERENCES skills_skill(id) ON DELETE CASCADE,
    difficulty VARCHAR(20) NOT NULL CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    title VARCHAR(200) NOT NULL,
    time_limit_minutes INTEGER NOT NULL DEFAULT 30,
    passing_score INTEGER NOT NULL DEFAULT 70 CHECK (passing_score BETWEEN 0 AND 100),
    questions JSONB NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- 4.11 verification.ExamAttempt
CREATE TABLE verification_examattempt (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    exam_id INTEGER NOT NULL REFERENCES verification_skillexam(id) ON DELETE CASCADE,
    score FLOAT NOT NULL,
    passed BOOLEAN NOT NULL DEFAULT FALSE,
    answers JSONB NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE NULL,
    can_retake_after TIMESTAMP WITH TIME ZONE NULL
);

-- 4.12 portfolio.Project
CREATE TABLE portfolio_project (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    project_url VARCHAR(200) NULL,
    image VARCHAR(100) NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- 4.13 portfolio.Certification
CREATE TABLE portfolio_certification (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_userprofile(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    issuing_organization VARCHAR(200) NOT NULL,
    issue_date DATE NOT NULL,
    certificate_file VARCHAR(100) NULL,
    verification_url VARCHAR(200) NULL
);

-- Performance indexes for JOINs and common queries
CREATE INDEX idx_skills_teachableskill_user ON skills_teachableskill(user_id);
CREATE INDEX idx_skills_teachableskill_skill ON skills_teachableskill(skill_id);
CREATE INDEX idx_skills_learnableskill_user ON skills_learnableskill(user_id);
CREATE INDEX idx_skills_learnableskill_skill ON skills_learnableskill(skill_id);
CREATE INDEX idx_exchanges_exchangeproposal_proposer ON exchanges_exchangeproposal(proposer_id);
CREATE INDEX idx_exchanges_exchangeproposal_receiver ON exchanges_exchangeproposal(receiver_id);
CREATE INDEX idx_exchanges_exchangeproposal_status ON exchanges_exchangeproposal(status);
CREATE INDEX idx_exchanges_exchangeproposal_offer_skill ON exchanges_exchangeproposal(offer_skill_id);
CREATE INDEX idx_exchanges_exchangeproposal_request_skill ON exchanges_exchangeproposal(request_skill_id);
CREATE INDEX idx_exchanges_exchangesession_proposal ON exchanges_exchangesession(proposal_id);
CREATE INDEX idx_exchanges_exchangesession_teacher ON exchanges_exchangesession(teacher_id);
CREATE INDEX idx_exchanges_exchangesession_learner ON exchanges_exchangesession(learner_id);
CREATE INDEX idx_exchanges_exchangesession_completed ON exchanges_exchangesession(completed);
CREATE INDEX idx_exchanges_skillcredittransaction_user ON exchanges_skillcredittransaction(user_id);
CREATE INDEX idx_exchanges_skillcredittransaction_type ON exchanges_skillcredittransaction(transaction_type);
CREATE INDEX idx_exchanges_skillcredittransaction_created ON exchanges_skillcredittransaction(created_at);
CREATE INDEX idx_verification_skillverification_user_skill ON verification_skillverification(user_id, skill_id);
CREATE INDEX idx_verification_certificate_user ON verification_certificate(user_id);
CREATE INDEX idx_verification_certificate_status ON verification_certificate(status);
CREATE INDEX idx_verification_skillexam_skill ON verification_skillexam(skill_id);
CREATE INDEX idx_verification_examattempt_user ON verification_examattempt(user_id);
CREATE INDEX idx_verification_examattempt_exam ON verification_examattempt(exam_id);
CREATE INDEX idx_portfolio_project_user ON portfolio_project(user_id);
CREATE INDEX idx_portfolio_certification_user ON portfolio_certification(user_id);
