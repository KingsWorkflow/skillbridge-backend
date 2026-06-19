from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.skills.models import TeachableSkill, LearnableSkill


@login_required
def project_list(request):
    """Display all user's projects."""
    projects = request.user.projects.all()
    return render(request, 'portfolio/project_list.html', {'projects': projects})


@login_required
def portfolio_view(request):
    user = request.user

    context = {
        'user': user,
        'profile': user,
        'projects': user.projects.all(),
        'certifications': user.certifications.all(),
        'achievements': [],
        'teachable_skills': TeachableSkill.objects.filter(
            user=user, is_active=True
        ).select_related('skill'),
        'learnable_skills': LearnableSkill.objects.filter(
            user=user
        ).select_related('skill'),
    }
    return render(request, 'portfolio/portfolio.html', context)