from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import ExamAnswerForm
from .models import SkillVerification, SkillExam, Question, ExamAttempt, Certificate
from apps.skills.models import Skill


@login_required
def verify_community(request, user_id, skill_id):
    """Render community verification page."""
    skill = get_object_or_404(Skill, id=skill_id)
    verification, created = SkillVerification.objects.get_or_create(
        user_id=user_id,
        skill=skill,
    )
    if created:
        verification.self_declared_at = timezone.now()
        verification.save()
    return render(request, 'verification/community_verify.html', {
        'skill': skill,
        'user_id': user_id,
        'verification': verification,
    })


@login_required
def start_exam(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    exam = SkillExam.objects.filter(skill=skill, is_active=True).first()

    if not exam:
        return render(request, 'verification/exam_start.html', {
            'form': None,
            'exam': None,
            'skill': skill,
            'blocked': False,
            'no_exam': True,
        })

    previous_attempt = ExamAttempt.objects.filter(
        user=request.user, exam=exam
    ).order_by('-started_at').first()

    blocked = False
    if previous_attempt and previous_attempt.can_retake_after and timezone.now() < previous_attempt.can_retake_after:
        blocked = True

    questions_qs = exam.questions.all().order_by('order')
    questions_data = [
        {
            'id': q.id,
            'text': q.text,
            'question_type': q.question_type,
            'options': q.options,
            'correct_index': q.correct_index,
            'model_answer': q.model_answer,
            'weight': q.weight,
        }
        for q in questions_qs
    ]

    if request.method == 'POST' and not blocked:
        form = ExamAnswerForm(questions_data, request.POST)
        if form.is_valid():
            answers = {}
            for q in questions_qs:
                answers[f'question_{q.id}'] = request.POST.get(f'question_{q.id}', '')

            total_weight = sum(q.weight for q in questions_qs)
            earned_marks = 0
            for q in questions_qs:
                student_answer = answers.get(f'question_{q.id}')
                if student_answer is not None and q.question_type == 'objective':
                    try:
                        if int(student_answer) == q.correct_index:
                            earned_marks += q.weight
                    except (ValueError, TypeError):
                        pass

            score = round((earned_marks / total_weight) * 100, 2) if total_weight > 0 else 0
            passed = score >= exam.passing_score

            attempt = ExamAttempt.objects.create(
                user=request.user,
                exam=exam,
                answers=answers,
                started_at=timezone.now(),
                completed_at=timezone.now(),
                score=score,
                passed=passed,
                can_retake_after=timezone.now() + timedelta(days=30),
            )
            messages.success(request, f'Exam submitted! Score: {score}%')
            return redirect('verification:exam_submit')
    else:
        form = ExamAnswerForm(questions_data)

    return render(request, 'verification/exam_start.html', {
        'form': form,
        'exam': exam,
        'skill': skill,
        'blocked': blocked,
        'retake_after': previous_attempt.can_retake_after if previous_attempt else None,
    })


@login_required
def exam_submit(request):
    last_attempt = ExamAttempt.objects.filter(
        user=request.user
    ).order_by('-started_at').first()
    return render(request, 'verification/exam_submit.html', {
        'attempt': last_attempt,
        'exam': last_attempt.exam if last_attempt else None,
    })


@login_required
def verification_status(request):
    from .models import Certificate

    verifications = SkillVerification.objects.filter(
        user=request.user
    ).select_related('skill').order_by('-current_level', 'skill__name')
    existing_skill_ids = {v.skill_id for v in verifications}

    approved_certificates = Certificate.objects.filter(
        user=request.user, status='approved'
    ).select_related('skill')

    for cert in approved_certificates:
        if cert.skill_id not in existing_skill_ids:
            synthetic = SkillVerification(
                user=request.user,
                skill=cert.skill,
                current_level=3,
                certificate_verified_at=datetime.combine(cert.issue_date, datetime.min.time()),
            )
            existing_skill_ids.add(cert.skill_id)
            verifications = list(verifications) + [synthetic]

    return render(request, 'verification/verification_status.html', {
        'verifications': verifications,
    })


@login_required
def certificate_list(request):
    certificates = Certificate.objects.filter(
        user=request.user,
        status='approved',
    ).select_related('skill').order_by('-issue_date')
    return render(request, 'verification/certificate_list.html', {
        'certificates': certificates,
    })
