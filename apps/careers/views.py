from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.cache import cache
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from apps.recommendations.recommendation_engine import recommend_careers


class CareerRecommendationView(View):
    """Display AI-powered career recommendations based on user's teachable skills."""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')

        cache_key = f'career_recommendations_{request.user.id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            context = cached_data
            context['from_cache'] = True
        else:
            recommendations = recommend_careers(request.user, top_n=5)
            for rec in recommendations:
                ordered = []
                for skill in rec.get('missing_skills', []):
                    hours = None
                    skill_id = getattr(skill, 'id', None)
                    skill_name = getattr(skill, 'name', str(skill))
                    hours_map = rec.get('estimated_hours_per_skill', {}) or {}
                    hours = hours_map.get(skill_name) or hours_map.get(str(skill_id))
                    ordered.append({
                        'name': skill_name,
                        'estimated_hours': hours,
                    })
                ordered.sort(key=lambda item: (item['estimated_hours'] is None, item['estimated_hours'] if item['estimated_hours'] is not None else 0))
                rec['missing_skills_ordered'] = ordered
            context = {
                'recommendations': recommendations,
                'from_cache': False,
            }
            # Cache for 24 hours
            cache.set(cache_key, context, timeout=60 * 60 * 24)

        return render(request, 'careers/career.html', context)


class RefreshRecommendationsView(View):
    """Clear cached recommendations and recompute."""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')

        cache_key = f'career_recommendations_{request.user.id}'
        cache.delete(cache_key)
        messages.success(request, 'Career recommendations refreshed successfully!')
        return redirect('careers:career_recommendations')
