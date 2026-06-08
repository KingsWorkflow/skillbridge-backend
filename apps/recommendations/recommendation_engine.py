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
from apps.skills.models import Skill


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
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        feature_matrix = vectorizer.fit_transform(user_features)
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
    
    if SKLEARN_AVAILABLE and vectorizer is not None:
        # Calculate similarity with all other users using TF-IDF
        target_features = features[target_idx]
        similarities = cosine_similarity(target_features, features).flatten()
        
        # Get indices sorted by similarity (descending)
        similar_indices = np.argsort(similarities)[::-1]
        
        for idx in similar_indices:
            if idx == target_idx:
                continue  # Skip the user themselves
            
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
    else:
        # Simple matching without sklearn
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
                # Simple similarity based on skill overlap
                similarity = (len(i_teach_they_learn) + len(i_learn_they_teach)) / max(len(target_teaches) + len(target_learns), 1)
                partners.append({
                    'partner_user': similar_user,
                    'similarity_score': similarity,
                    'mutual_match_score': len(i_teach_they_learn) + len(i_learn_they_teach),
                    'i_teach_they_learn': list(i_teach_they_learn),
                    'i_learn_they_teach': list(i_learn_they_teach),
                })
    
    # Sort by similarity score and return top N
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