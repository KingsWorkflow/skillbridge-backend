from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def career_recommendations(request):
    return render(request, 'recommendations/career_recommendations.html', {
        'career_matches': [],
    })

@login_required
def skill_recommendations(request):
    return render(request, 'recommendations/skill_recommendations.html', {
        'skill_matches': [],
    })

@login_required
def roadmap_view(request):
    return render(request, 'recommendations/roadmap.html', {
        'roadmap': [],
    })

@login_required
def skill_gap(request):
    return render(request, 'recommendations/skill_gap.html', {
        'priority_goals': [],
        'mentors': [],
    })

def resources(request):
    return render(request, 'recommendations/resources.html', {
        'trending_careers': [],
        'internships': [],
    })