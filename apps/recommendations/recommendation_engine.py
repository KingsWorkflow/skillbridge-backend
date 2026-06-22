"""
AI Recommendation Engine for SkillBridge using TF-IDF and cosine similarity.
"""

import numpy as np

# Try to import sklearn, fall back to simple matching if not available
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from django.contrib.auth import get_user_model
from apps.skills.models import Skill, TeachableSkill
from apps.careers.models import CareerPath

User = get_user_model()


def build_user_feature_matrix():
    """Build a feature matrix representing each user's skills.
    
    Returns:
        tuple: (user_ids, feature_matrix, vectorizer)
    """
    users = User.objects.prefetch_related(
        'teachable_skills__skill',
        'learnable_skills__skill'
    ).all()
    
    user_ids = []
    user_features = []
    
    for user in users:
        user_ids.append(user.id)
        
        # Create a text representation of user's skills
        skills_text = []
        
        # Add teachable skills
        for ts in user.teachable_skills.all():
            skills_text.append(f"teach:{ts.skill.name}")
        
        # Add learnable skills
        for ls in user.learnable_skills.all():
            skills_text.append(f"learn:{ls.skill.name}")
        
        user_features.append(' '.join(skills_text) if skills_text else '')
    
    if SKLEARN_AVAILABLE:
        # Create TF-IDF vectorizer (handle empty or all-empty features)
        vectorizer = TfidfVectorizer()
        non_empty_features = [f for f in user_features if f.strip()]
        if non_empty_features and len(non_empty_features) > 0:
            try:
                feature_matrix = vectorizer.fit_transform(user_features)
            except ValueError:
                feature_matrix = None
        else:
            feature_matrix = None
        return user_ids, feature_matrix, vectorizer
    else:
        return user_ids, user_features, None


def find_exchange_partners(user_id, top_n=10):
    """Find potential exchange partners for a given user.
    
    Args:
        user_id: The ID of the user to find partners for
        top_n: Maximum number of partners to return
    
    Returns:
        list: List of dictionaries with partner info
    """
    user_ids, features, vectorizer = build_user_feature_matrix()
    
    # Find the index of the target user
    try:
        target_idx = user_ids.index(user_id)
    except ValueError:
        return []
    
    target_user = User.objects.prefetch_related(
        'teachable_skills__skill',
        'learnable_skills__skill'
    ).get(id=user_id)
    
    # Get the target user's skills
    target_teaches = set(target_user.teachable_skills.values_list('skill_id', flat=True))
    target_learns = set(target_user.learnable_skills.values_list('skill_id', flat=True))
    
    partners = []
    
    # Use sklearn if available and features exist
    if SKLEARN_AVAILABLE and features is not None:
        try:
            target_features = features[target_idx]
            similarities = cosine_similarity(target_features, features).flatten()
            
            # Get indices sorted by similarity (descending)
            similar_indices = np.argsort(similarities)[::-1]
            
            for idx in similar_indices:
                if idx == target_idx:
                    continue
                
                partner_id = user_ids[idx]
                similar_user = User.objects.prefetch_related(
                    'teachable_skills__skill',
                    'learnable_skills__skill'
                ).get(id=partner_id)
                
                similar_teaches = set(similar_user.teachable_skills.values_list('skill_id', flat=True))
                similar_learns = set(similar_user.learnable_skills.values_list('skill_id', flat=True))
                
                i_teach_they_learn = target_teaches & similar_learns
                i_learn_they_teach = target_learns & similar_teaches
                
                if i_teach_they_learn or i_learn_they_teach:
                    partners.append({
                        'partner_user': similar_user,
                        'similarity_score': float(similarities[idx]),
                        'mutual_match_score': len(i_teach_they_learn) + len(i_learn_they_teach),
                        'i_teach_they_learn': list(i_teach_they_learn),
                        'i_learn_they_teach': list(i_learn_they_teach),
                    })
                
                if len(partners) >= top_n:
                    break
        except Exception:
            pass
    
    # Simple matching fallback
    if not partners:
        for i, partner_id in enumerate(user_ids):
            if partner_id == user_id:
                continue
            
            similar_user = User.objects.prefetch_related(
                'teachable_skills__skill',
                'learnable_skills__skill'
            ).get(id=partner_id)
            
            similar_teaches = set(similar_user.teachable_skills.values_list('skill_id', flat=True))
            similar_learns = set(similar_user.learnable_skills.values_list('skill_id', flat=True))
            
            i_teach_they_learn = target_teaches & similar_learns
            i_learn_they_teach = target_learns & similar_teaches
            
            if i_teach_they_learn or i_learn_they_teach:
                similarity = (len(i_teach_they_learn) + len(i_learn_they_teach)) / max(len(target_teaches) + len(target_learns), 1)
                partners.append({
                    'partner_user': similar_user,
                    'similarity_score': similarity,
                    'mutual_match_score': len(i_teach_they_learn) + len(i_learn_they_teach),
                    'i_teach_they_learn': list(i_teach_they_learn),
                    'i_learn_they_teach': list(i_learn_they_teach),
                })
    
    partners.sort(key=lambda x: x['similarity_score'], reverse=True)
    return partners[:top_n]


def resolve_skill_ids_to_names(partners):
    """Convert skill IDs in partners list to skill names."""
    skill_ids = set()
    for p in partners:
        skill_ids.update(p['i_teach_they_learn'])
        skill_ids.update(p['i_learn_they_teach'])
    
    skill_map = {s.id: s.name for s in Skill.objects.filter(id__in=skill_ids)}
    
    for p in partners:
        p['i_teach_they_learn'] = [skill_map.get(sid, str(sid)) for sid in p['i_teach_they_learn']]
        p['i_learn_they_teach'] = [skill_map.get(sid, str(sid)) for sid in p['i_learn_they_teach']]
    
    return partners


def recommend_careers(user, top_n=5):
    """Recommend career paths based on user's teachable skills using cosine similarity.
    
    Args:
        user: User instance
        top_n: Maximum number of career recommendations to return
    
    Returns:
        list: List of dictionaries with career recommendation info
    """
    user_teachable_ids = set(user.teachable_skills.values_list('skill_id', flat=True))
    if not user_teachable_ids:
        # No skills adds no match signal; return empty recommendations
        return []
    user_skill_ids = user_teachable_ids

    careers = CareerPath.objects.prefetch_related('required_skills').all()
    results = []

    all_skill_ids = set(Skill.objects.values_list('id', flat=True))

    for career in careers:
        required_ids = set(career.required_skills.values_list('id', flat=True))
        if not required_ids:
            continue

        overlap = user_skill_ids & required_ids
        match_score = (len(overlap) / len(required_ids)) * 100

        missing_skills = career.required_skills.exclude(id__in=user_skill_ids)
        matched_skills = career.required_skills.filter(id__in=user_skill_ids)

        estimated_hours_per_skill = {}
        if career.estimated_hours_per_skill:
            estimated_hours_per_skill = career.estimated_hours_per_skill

        results.append({
            'career': career,
            'match_score': float(match_score),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'required_skills_count': required_ids.__len__(),
            'estimated_hours_per_skill': estimated_hours_per_skill,
            'title': career.title,
            'description': career.description,
            'category': career.category,
            'average_salary': career.average_salary,
            'growth_outlook': career.growth_outlook,
            'matched_skill_names': [s.name for s in matched_skills],
        })

    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results[:top_n]


PROFICIENCY_TO_LEVEL = {
    'beginner': 25,
    'intermediate': 50,
    'expert': 75,
}

PRIORITY_ICONS = {
    'Technology': 'code',
    'Data': 'analytics',
    'Management': 'groups',
    'Design': 'palette',
    'Marketing': 'campaign',
}


def get_careers_list():
    """Return list of available career paths for the selector."""
    return list(CareerPath.objects.values_list('title', flat=True).order_by('title'))


def compute_skill_gap(user, target_career_title=None, custom_goals=None, hidden_skill_ids=None):
    """Compute skill gap analysis for a user against a target career.
    
    Returns dict with match_score, target_career, priority_goals, mentors, chart_data.
    custom_goals: list of dicts with keys skill, missing, progress, color, icon (user-added)
    hidden_skill_ids: set of skill IDs to exclude from priority goals (user-dismissed)
    """
    custom_goals = custom_goals or []
    hidden_skill_ids = set(hidden_skill_ids or [])
    if not target_career_title:
        target_career_title = 'Full Stack Developer'
    
    career = CareerPath.objects.filter(title__icontains=target_career_title).first()
    if not career:
        career = CareerPath.objects.first()
    if not career:
        return {
            'match_score': 0,
            'target_career': target_career_title,
            'priority_goals': list(custom_goals),
            'mentors': [],
            'chart_data': {'labels': [], 'user': [], 'market': []},
        }
    
    required_skills = career.required_skills.all()
    user_teachable = user.teachable_skills.filter(is_active=True).select_related('skill')
    user_teachable_map = {ts.skill_id: ts for ts in user_teachable}
    
    required_ids = list(required_skills.values_list('id', flat=True))
    matched_ids = [sid for sid in required_ids if sid in user_teachable_map]
    missing_ids = [sid for sid in required_ids if sid not in user_teachable_map]
    match_score = (len(matched_ids) / len(required_ids)) * 100 if required_ids else 0
    
    chart_skills = list(required_skills[:6])
    chart_labels = [s.name for s in chart_skills]
    chart_user = []
    chart_market = []
    
    for skill in chart_skills:
        chart_market.append(80)
        if skill.id in user_teachable_map:
            chart_user.append(PROFICIENCY_TO_LEVEL.get(user_teachable_map[skill.id].proficiency_level, 25))
        else:
            chart_user.append(5)
    
    custom_goal_keys = {(g['skill'], g.get('missing', '')) for g in custom_goals}
    
    priority_goals = []
    for g in custom_goals:
        priority_goals.append({**g, 'is_custom': True})
    for skill in required_skills.filter(id__in=missing_ids):
        if skill.id in hidden_skill_ids:
            continue
        estimated_hours = None
        if career.estimated_hours_per_skill:
            estimated_hours = career.estimated_hours_per_skill.get(str(skill.id)) or career.estimated_hours_per_skill.get(skill.name)
        priority_goals.append({
            'skill': skill.name,
            'skill_id': skill.id,
            'missing': 'Not yet acquired',
            'progress': 0,
            'color': 'tertiary',
            'icon': PRIORITY_ICONS.get(skill.category, 'terminal'),
            'estimated_hours': estimated_hours,
        })
    
    mentors = []
    if missing_ids:
        missing_teachers = TeachableSkill.objects.filter(
            skill_id__in=missing_ids,
            is_active=True,
        ).select_related('user', 'skill')
        mentor_users = {}
        for mt in missing_teachers:
            uid = mt.user_id
            if uid not in mentor_users and uid != user.id:
                mentor_users[uid] = mt
        
        for uid, mt in mentor_users.items():
            mentor_skills = list(TeachableSkill.objects.filter(user_id=uid, is_active=True).select_related('skill')[:3])
            avatar = mt.user.profile_picture
            avatar_url = avatar.url if avatar and hasattr(avatar, 'url') else None
            mentors.append({
                'name': mt.user.get_full_name() or mt.user.username,
                'title': mt.user.title or 'Community Member',
                'avatar': avatar_url,
                'skills': [ms.skill.name for ms in mentor_skills],
                'closed_gaps': mt.user.reputation_score,
                'user_id': uid,
                'gap_skill': mt.skill.name,
                'gap_skill_id': mt.skill_id,
            })
        
        mentors.sort(key=lambda x: x['closed_gaps'], reverse=True)
        mentors = mentors[:6]
    
    return {
        'match_score': int(round(match_score, 0)),
        'target_career': career.title,
        'priority_goals': priority_goals[:8],
        'mentors': mentors[:3],
        'chart_data': {
            'labels': chart_labels,
            'user': chart_user,
            'market': chart_market,
        },
    }
