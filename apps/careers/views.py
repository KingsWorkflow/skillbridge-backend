from django.shortcuts import render
from django.views import View
from django.core.cache import cache
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from apps.recommendations.recommendation_engine import recommend_careers


def _serialize_recommendation(rec):
    """Convert a raw recommendation dict into a cache-safe plain dict."""
    missing_ordered = []
    missing_skills = rec.get('missing_skills')
    if missing_skills is not None:
        for skill in missing_skills:
            skill_name = getattr(skill, 'name', str(skill))
            skill_id = getattr(skill, 'id', None)
            hours_map = rec.get('estimated_hours_per_skill', {}) or {}
            hours = hours_map.get(skill_name) or hours_map.get(str(skill_id))
            missing_ordered.append({
                'name': skill_name,
                'estimated_hours': hours,
            })
        missing_ordered.sort(key=lambda item: (
            item['estimated_hours'] is None,
            item['estimated_hours'] if item['estimated_hours'] is not None else 0
        ))

    matched_skills = []
    matched_qs = rec.get('matched_skills')
    if matched_qs is not None:
        matched_skills = [getattr(s, 'name', str(s)) for s in matched_qs]

    return {
        'title': rec.get('title', ''),
        'description': rec.get('description', ''),
        'category': rec.get('category', ''),
        'match_score': float(rec.get('match_score', 0)),
        'average_salary': rec.get('average_salary', ''),
        'growth_outlook': rec.get('growth_outlook', ''),
        'required_skills_count': rec.get('required_skills_count', 0),
        'matched_skills': matched_skills,
        'missing_skills_ordered': missing_ordered,
    }


class CareerRecommendationView(View):
    """Display career recommendations based on user's teachable skills."""

    CACHE_TIMEOUT = 60 * 60  # 1 hour

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')

        cache_key = f'career_recommendations_{request.user.id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            recommendations = cached_data.get('recommendations', [])
            is_from_cache = True
        else:
            try:
                raw_recommendations = recommend_careers(request.user, top_n=5)
            except Exception:
                raw_recommendations = []

            recommendations = [_serialize_recommendation(rec) for rec in raw_recommendations]
            cache_payload = {'recommendations': recommendations}
            cache.set(cache_key, cache_payload, timeout=self.CACHE_TIMEOUT)
            is_from_cache = False

        return render(request, 'careers/career.html', {
            'recommendations': recommendations,
            'from_cache': is_from_cache,
        })


def api_career_recommendations(request):
    """JSON API endpoint for career recommendations."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    cache_key = f'career_recommendations_api_{request.user.id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data)

    try:
        raw_recommendations = recommend_careers(request.user, top_n=5)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    recommendations = [_serialize_recommendation(rec) for rec in raw_recommendations]
    response_data = {
        'recommendations': recommendations,
        'count': len(recommendations),
    }
    cache.set(cache_key, response_data, timeout=60 * 60)
    return JsonResponse(response_data)


class RefreshRecommendationsView(View):
    """Clear cached recommendations and recompute."""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')

        cache_key = f'career_recommendations_{request.user.id}'
        cache.delete(cache_key)
        messages.success(request, 'Career recommendations refreshed successfully!')
        return redirect('careers:career_recommendations')
