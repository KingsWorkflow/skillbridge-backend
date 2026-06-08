from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .recommendation_engine import find_exchange_partners as ai_find_exchange_partners, resolve_skill_ids_to_names


@login_required
def exchange_partners(request):
    """Find and display potential exchange partners using AI recommendations."""
    partners = ai_find_exchange_partners(request.user.id, top_n=10)
    partners = resolve_skill_ids_to_names(partners)
    return render(request, 'recommendations/partners.html', {'partners': partners})


def api_partners(request):
    """API endpoint for AJAX calls."""
    if request.user.is_authenticated:
        partners = ai_find_exchange_partners(request.user.id, top_n=10)
        partners = resolve_skill_ids_to_names(partners)
        # Convert partners to serializable format
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
    return JsonResponse({'partners': []})


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
        'skill_matches': [
            {'name': 'Python', 'reason': 'High demand in Nepalese market', 'match_score': 95},
            {'name': 'Cloud Computing', 'reason': 'Growing sector', 'match_score': 88},
            {'name': 'UI Design', 'reason': 'Creative tech skills', 'match_score': 82},
        ],
    })


def skill_gap(request):
    """Skill gap analysis page."""
    return render(request, 'recommendations/skill_gap.html', {})