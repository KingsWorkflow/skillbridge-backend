from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .recommendation_engine import find_exchange_partners as ai_find_exchange_partners, resolve_skill_ids_to_names, compute_skill_gap, get_careers_list
from apps.skills.models import Skill
from apps.careers.models import CareerPath
from apps.users.models import UserProfile
from apps.portfolio.models import Project, Certification


@login_required
def exchange_partners(request):
    """Find and display potential exchange partners using AI recommendations."""
    partners = ai_find_exchange_partners(request.user.id, top_n=10)
    partners = resolve_skill_ids_to_names(partners)
    return render(request, 'recommendations/partners.html', {'partners': partners})


@login_required
def api_partners(request):
    """API endpoint for AJAX calls."""
    partners = ai_find_exchange_partners(request.user.id, top_n=10)
    partners = resolve_skill_ids_to_names(partners)
    serialized_partners = []
    for p in partners:
        serialized_partners.append({
            'partner_user': {
                'id': p['partner_user'].id,
                'username': p['partner_user'].username,
                'skill_credits': p['partner_user'].skill_credits,
            },
            'similarity_score': p['similarity_score'],
            'mutual_match_score': p['mutual_match_score'],
            'i_teach_they_learn': p['i_teach_they_learn'],
            'i_learn_they_teach': p['i_learn_they_teach'],
        })
    return JsonResponse({'partners': serialized_partners})


def get_exchange_partners(user_id, top_n=10):
    """Wrapper for backward compatibility."""
    partners = ai_find_exchange_partners(user_id, top_n)
    return resolve_skill_ids_to_names(partners)


def resources(request):
    """Resources page showing trending careers and opportunities."""
    return render(request, 'recommendations/resources.html', {
        'trending_careers': [
            {'title': 'Full-Stack Developer', 'description': 'Build web applications from front to back', 'growth': '+25% YoY'},
            {'title': 'Data Scientist', 'description': 'Extract insights from data', 'growth': '+35% YoY'},
            {'title': 'Product Manager', 'description': 'Lead product development', 'growth': '+20% YoY'},
            {'title': 'UX Designer', 'description': 'Design user experiences', 'growth': '+30% YoY'},
        ],
        'internships': [
            {'title': 'Software Engineering Intern', 'company': 'TechCorp Nepal', 'location': 'Kathmandu', 'type': 'Remote'},
            {'title': 'Data Analyst Intern', 'company': 'DataLabs', 'location': 'Remote', 'type': 'Part-time'},
            {'title': 'UI/UX Intern', 'company': 'DesignStudio', 'location': 'Lalitpur', 'type': 'On-site'},
        ],
    })


def career_recommendations(request):
    """AI-powered career recommendations."""
    return render(request, 'recommendations/career_recommendations.html', {
        'career_matches': [
            {'title': 'Python Developer', 'reason': 'High demand in Nepalese market', 'match_score': 95, 'growth': '+25% YoY', 'skills_required': ['Python', 'Django', 'REST API']},
            {'title': 'Cloud Computing', 'reason': 'Growing sector', 'match_score': 88, 'growth': '+30% YoY', 'skills_required': ['AWS', 'Azure', 'Docker']},
            {'title': 'UI Design', 'reason': 'Creative tech skills', 'match_score': 82, 'growth': '+20% YoY', 'skills_required': ['Figma', 'UX', 'Prototyping']},
        ],
    })


@login_required
def skill_gap(request):
    """Skill gap analysis page."""
    target_career = request.GET.get('target_career', '')
    custom_goals = request.session.get('custom_priority_goals', [])
    hidden_skill_ids = request.session.get('hidden_priority_skill_ids', [])
    data = compute_skill_gap(request.user, target_career if target_career else None, custom_goals=custom_goals, hidden_skill_ids=hidden_skill_ids)
    return render(request, 'recommendations/skill_gap.html', {
        'target_career': data['target_career'],
        'match_score': data['match_score'],
        'priority_goals': data['priority_goals'],
        'mentors': data['mentors'],
        'chart_data': data['chart_data'],
        'available_careers': get_careers_list(),
    })


@login_required
def skill_gap_api(request):
    """JSON API for skill gap data.
    GET  → returns full analysis (optionally filtered by ?target_career=).
    POST → mutates custom goals (action=add|remove) and returns updated analysis.
    """
    body = {}
    goals = list(request.session.get('custom_priority_goals', []))

    if request.method == 'POST':
        try:
            import json as _json
            body_data = request.body
            body = _json.loads(body_data.decode('utf-8')) if body_data else {}
            action = body.get('action', '')

            if action == 'add':
                skill = body.get('skill', '').strip()
                missing = body.get('missing', 'Custom goal').strip()
                progress = int(body.get('progress', 0))
                color = body.get('color', 'tertiary')
                icon = body.get('icon', 'flag')
                if skill:
                    goals.append({'skill': skill, 'missing': missing, 'progress': progress, 'color': color, 'icon': icon})
            elif action == 'remove':
                index = int(body.get('index', -1))
                if 0 <= index < len(goals):
                    goals.pop(index)
            elif action == 'dismiss':
                skill_id = body.get('skill_id')
                if skill_id is not None:
                    try:
                        skill_id_int = int(skill_id)
                        hidden = list(request.session.get('hidden_priority_skill_ids', []))
                        if skill_id_int not in hidden:
                            hidden.append(skill_id_int)
                        request.session['hidden_priority_skill_ids'] = hidden
                        request.session.modified = True
                    except (ValueError, TypeError):
                        pass

            request.session['custom_priority_goals'] = goals
            request.session.modified = True
        except Exception:
            pass

    target_career = request.GET.get('target_career', '') or body.get('target_career', '') or ''
    hidden_skill_ids = request.session.get('hidden_priority_skill_ids', [])
    data = compute_skill_gap(
        request.user,
        target_career if target_career else None,
        custom_goals=goals,
        hidden_skill_ids=hidden_skill_ids,
    )
    return JsonResponse(data)


@login_required
def careers_list_api(request):
    """JSON API listing all available career paths."""
    return JsonResponse({'careers': get_careers_list()})


def search(request):
    """Global search across skills, careers, people, projects, and certifications."""
    q = request.GET.get('q', '').strip()
    results = {
        'skills': [],
        'careers': [],
        'people': [],
        'projects': [],
        'certifications': [],
    }
    if q:
        results['skills'] = Skill.objects.filter(
            Q(name__icontains=q) | Q(category__icontains=q)
        ).order_by('-popularity_score')[:10]

        results['careers'] = CareerPath.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        ).order_by('title')[:10]

        results['people'] = UserProfile.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(username__icontains=q) |
            Q(title__icontains=q) |
            Q(bio__icontains=q) |
            Q(location__icontains=q)
        ).filter(is_active=True).order_by('-reputation_score')[:10]

        results['projects'] = Project.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        ).select_related('user').order_by('-created_at')[:10]

        results['certifications'] = Certification.objects.filter(
            Q(name__icontains=q) | Q(issuing_organization__icontains=q)
        ).select_related('user').order_by('-issue_date')[:10]

    return render(request, 'recommendations/search.html', {
        'query': q,
        'results': results,
    })


def api_search(request):
    """JSON API for search suggestions."""
    q = request.GET.get('q', '').strip()
    suggestions = []
    if q and len(q) >= 2:
        skills = Skill.objects.filter(name__icontains=q).order_by('-popularity_score').values_list('name', flat=True)[:5]
        suggestions.extend([{'type': 'skill', 'text': s} for s in skills])
        careers = CareerPath.objects.filter(title__icontains=q).order_by('title').values_list('title', flat=True)[:3]
        suggestions.extend([{'type': 'career', 'text': c} for c in careers])
        people = UserProfile.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q)
        ).filter(is_active=True).order_by('-reputation_score').values_list('username', flat=True)[:3]
        suggestions.extend([{'type': 'person', 'text': p} for p in people])
    return JsonResponse({'suggestions': suggestions})
