from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import json

from apps.skills.models import Skill
from .models import SkillVerification, SkillExam, Question, ExamAttempt
from .serializers import (
    SkillVerificationSerializer,
    SkillExamSerializer,
    ExamAttemptSerializer,
)


@login_required
def api_verification_status(request):
    verifications = SkillVerification.objects.filter(user=request.user).select_related('skill')
    serializer = SkillVerificationSerializer(verifications, many=True)
    return JsonResponse({'results': serializer.data})


@login_required
def api_exam_list(request):
    skill_id = request.GET.get('skill_id')
    exams = SkillExam.objects.filter(is_active=True).select_related('skill')
    if skill_id:
        exams = exams.filter(skill_id=skill_id)
    serializer = SkillExamSerializer(exams, many=True)
    return JsonResponse({'results': serializer.data})


@login_required
def api_exam_detail(request, exam_id):
    exam = get_object_or_404(SkillExam, id=exam_id, is_active=True)
    serializer = SkillExamSerializer(exam)
    return JsonResponse(serializer.data)


@login_required
def api_exam_start(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    exam = get_object_or_404(SkillExam, skill=skill, is_active=True)

    previous_attempt = ExamAttempt.objects.filter(
        user=request.user, exam=exam
    ).order_by('-started_at').first()

    if (previous_attempt and previous_attempt.can_retake_after
            and timezone.now() < previous_attempt.can_retake_after):
        return JsonResponse({
            'detail': 'You cannot retake this exam yet.',
            'retake_after': previous_attempt.can_retake_after.isoformat(),
        }, status=429)

    attempt = ExamAttempt.objects.create(
        user=request.user,
        exam=exam,
        answers={},
        started_at=timezone.now(),
    )
    serializer = ExamAttemptSerializer(attempt)
    return JsonResponse(serializer.data, status=201)


@login_required
def api_exam_submit(request, exam_id):
    exam = get_object_or_404(SkillExam, id=exam_id, is_active=True)

    try:
        body = request.body.decode('utf-8')
        answers = json.loads(body).get('answers', {}) if body else {}
    except (json.JSONDecodeError, Exception):
        return JsonResponse({'answers': ['Invalid request body.']}, status=400)

    questions = exam.questions.all().order_by('order')
    total_weight = sum(q.weight for q in questions)
    earned_marks = 0

    for q in questions:
        student_answer = answers.get(f'question_{q.id}')
        if student_answer is None:
            continue
        try:
            student_answer = int(student_answer)
        except (ValueError, TypeError):
            continue
        if student_answer == q.correct_index:
            earned_marks += q.weight

    if total_weight > 0:
        score = round((earned_marks / total_weight) * 100, 2)
    else:
        score = 0

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

    questions_data = []
    for q in exam.questions.all().order_by('order'):
        questions_data.append({
            'id': q.id,
            'text': q.text,
            'question_type': q.question_type,
            'options': q.options if q.question_type == 'objective' else [],
            'correct_index': q.correct_index if q.question_type == 'objective' else None,
            'model_answer': q.model_answer if q.question_type == 'subjective' else None,
            'weight': q.weight,
            'explanation': q.explanation or '',
            'order': q.order,
        })

    response_data = ExamAttemptSerializer(attempt).data
    response_data['questions'] = questions_data
    response_data['total_weight'] = exam.total_weight
    response_data['earned_marks'] = round((score / 100) * exam.total_weight, 2) if exam.total_weight > 0 else 0
    return JsonResponse(response_data, status=200)


@login_required
def api_community_verify(request, user_id, skill_id):
    if request.user.id == int(user_id):
        return JsonResponse(
            {'detail': 'You cannot verify your own skill.'},
            status=400,
        )

    skill = get_object_or_404(Skill, id=skill_id)
    verification, created = SkillVerification.objects.get_or_create(
        user_id=user_id,
        skill=skill,
    )

    if created:
        verification.self_declared_at = timezone.now()

    verification.verification_votes += 1

    if verification.verification_votes >= 3:
        verification.current_level = 2
        verification.community_verified_at = timezone.now()

    verification.save()
    serializer = SkillVerificationSerializer(verification)
    return JsonResponse(serializer.data, status=200)
