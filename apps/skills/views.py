from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Skill catalog views
def skill_list(request):
    return render(request, 'skills/skill_list.html', {
        'skills': [],
    })

@login_required
def teachable_skills(request):
    return render(request, 'skills/teachable_skills.html', {
        'teachable_skills': [],
    })

@login_required
def learnable_skills(request):
    return render(request, 'skills/learnable_skills.html', {
        'learnable_skills': [],
    })