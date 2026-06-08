from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TeachableSkillForm, LearnableSkillForm
from .models import Skill


def skill_list(request):
    return render(request, 'skills/skill_list.html', {
        'skills': Skill.objects.all(),
    })


@login_required
def teachable_skills(request):
    if request.method == 'POST':
        form = TeachableSkillForm(request.POST, user=request.user)
        if form.is_valid():
            teachable = form.save(commit=False)
            teachable.user = request.user
            teachable.save()
            messages.success(request, 'Teachable skill added successfully!')
            return redirect('skills:teachable')
    else:
        form = TeachableSkillForm(user=request.user)
    
    # Prepare skills for template
    teachable_list = []
    for ts in request.user.teachable_skills.select_related('skill').all():
        teachable_list.append({
            'name': ts.skill.name,
            'proficiency_level': ts.get_proficiency_level_display(),
            'hourly_commitment': ts.hourly_commitment,
        })
    
    return render(request, 'skills/teachable_skills.html', {
        'teachable_skills': teachable_list,
        'form': form,
        'all_skills': Skill.objects.all(),
    })


@login_required
def learnable_skills(request):
    if request.method == 'POST':
        form = LearnableSkillForm(request.POST, user=request.user)
        if form.is_valid():
            learnable = form.save(commit=False)
            learnable.user = request.user
            learnable.save()
            messages.success(request, 'Learnable skill added successfully!')
            return redirect('skills:learnable')
    else:
        form = LearnableSkillForm(user=request.user)
    
    # Prepare skills for template
    learnable_list = []
    for ls in request.user.learnable_skills.select_related('skill').all():
        learnable_list.append({
            'name': ls.skill.name,
            'urgency': ls.get_urgency_display(),
        })
    
    return render(request, 'skills/learnable_skills.html', {
        'learnable_skills': learnable_list,
        'form': form,
        'all_skills': Skill.objects.all(),
    })