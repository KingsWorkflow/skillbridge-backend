from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import TeachableSkillForm, LearnableSkillForm
from .models import Skill, TeachableSkill, LearnableSkill


def skill_list(request):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    skills = Skill.objects.all()
    if q:
        skills = skills.filter(name__icontains=q)
    if category:
        skills = skills.filter(category__iexact=category)
    categories = Skill.objects.values_list('category', flat=True).distinct().order_by('category')
    return render(request, 'skills/skill_list.html', {
        'skills': skills,
        'q': q,
        'category': category,
        'categories': categories,
    })


@login_required
def teachable_skills(request):
    if request.method == 'POST':
        form = TeachableSkillForm(request.POST, user=request.user)
        if form.is_valid():
            skill_id = form.cleaned_data.get('skill')
            proficiency = form.cleaned_data.get('proficiency_level')
            hours = form.cleaned_data.get('hourly_commitment')
            teachable, created = TeachableSkill.objects.get_or_create(
                user=request.user,
                skill=skill_id,
                defaults={'proficiency_level': proficiency, 'hourly_commitment': hours},
            )
            if created:
                messages.success(request, 'Teachable skill added successfully!')
            else:
                messages.info(request, 'This skill is already in your teachable list.')
            return redirect('skills:teachable_skills')
    else:
        form = TeachableSkillForm(user=request.user)

    teachable_list = request.user.teachable_skills.select_related('skill').all()

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
            skill_id = form.cleaned_data.get('skill')
            motivation = form.cleaned_data.get('motivation', '')
            urgency = form.cleaned_data.get('urgency', 'medium')
            learnable, created = LearnableSkill.objects.get_or_create(
                user=request.user,
                skill=skill_id,
                defaults={'motivation': motivation, 'urgency': urgency},
            )
            if created:
                messages.success(request, 'Learnable skill added successfully!')
            else:
                messages.info(request, 'This skill is already in your learnable list.')
            return redirect('skills:learnable_skills')
    else:
        form = LearnableSkillForm(user=request.user)

    learnable_list = request.user.learnable_skills.select_related('skill').all()

    return render(request, 'skills/learnable_skills.html', {
        'learnable_skills': learnable_list,
        'form': form,
        'all_skills': Skill.objects.all(),
    })


@login_required
@require_POST
def delete_teachable_skill(request, pk):
    skill = get_object_or_404(TeachableSkill, pk=pk, user=request.user)
    skill.delete()
    messages.success(request, 'Teachable skill removed.')
    return redirect('skills:teachable_skills')


@login_required
@require_POST
def delete_learnable_skill(request, pk):
    skill = get_object_or_404(LearnableSkill, pk=pk, user=request.user)
    skill.delete()
    messages.success(request, 'Learnable skill removed.')
    return redirect('skills:learnable_skills')


@login_required
@require_POST
def toggle_teachable_skill_active(request, pk):
    skill = get_object_or_404(TeachableSkill, pk=pk, user=request.user)
    skill.is_active = not skill.is_active
    skill.save()
    status = 'activated' if skill.is_active else 'deactivated'
    messages.success(request, f'Skill {status}.')
    return redirect('skills:teachable_skills')
