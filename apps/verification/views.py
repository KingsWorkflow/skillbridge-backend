from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import CertificateUploadForm, ExamAnswerForm
from .models import SkillVerification, Certificate, SkillExam, ExamAttempt
from apps.skills.models import Skill


@login_required
def upload_certificate(request):
    if request.method == 'POST':
        form = CertificateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.user = request.user
            cert.save()
            messages.success(request, 'Certificate uploaded! Awaiting admin approval.')
            return redirect('users:profile')
    else:
        form = CertificateUploadForm()
    return render(request, 'verification/certificate_upload.html', {'form': form})


@login_required
def verify_community(request, user_id, skill_id):
    """Allow users to verify another user's skill (community verification)."""
    skill = get_object_or_404(Skill, id=skill_id)
    verification, created = SkillVerification.objects.get_or_create(
        user_id=user_id,
        skill=skill
    )
    
    if created:
        verification.self_declared_at = timezone.now()
    
    verification.verification_votes += 1
    
    # If 3 votes reached, upgrade to level 2
    if verification.verification_votes >= 3:
        verification.current_level = 2
        verification.community_verified_at = timezone.now()
    
    verification.save()
    messages.success(request, 'Skill verified!')
    return redirect('recommendations:partners')


@login_required
def start_exam(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    exam = get_object_or_404(SkillExam, skill=skill, is_active=True)
    
    # Check if user can retake
    previous_attempt = ExamAttempt.objects.filter(
        user=request.user, 
        exam=exam
    ).order_by('-started_at').first()
    
    if previous_attempt and previous_attempt.can_retake_after and timezone.now() < previous_attempt.can_retake_after:
        messages.error(request, 'You cannot retake this exam yet.')
        return redirect('recommendations:partners')
    
    if request.method == 'POST':
        form = ExamAnswerForm(exam.questions, request.POST)
        if form.is_valid():
            score = 0
            # Simplified scoring - in real implementation would compare answers
            attempt = ExamAttempt.objects.create(
                user=request.user,
                exam=exam,
                answers={f'question_{i}': request.POST.get(f'question_{i}') for i in range(len(exam.questions))},
                started_at=timezone.now(),
                completed_at=timezone.now()
            )
            attempt.score = score
            attempt.passed = score >= exam.passing_score
            attempt.can_retake_after = timezone.now() + timedelta(days=30)
            attempt.save()
            
            if attempt.passed:
                messages.success(request, f'Exam passed! Score: {score}%')
            else:
                messages.error(request, f'Exam not passed. Score: {score}%')
            return redirect('recommendations:partners')
    else:
        form = ExamAnswerForm(exam.questions)
    
    return render(request, 'verification/exam_start.html', {'form': form, 'exam': exam})