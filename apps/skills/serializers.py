from rest_framework import serializers
from .models import Skill, TeachableSkill, LearnableSkill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'category', 'popularity_score')


class TeachableSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    category = serializers.CharField(source='skill.category', read_only=True)

    class Meta:
        model = TeachableSkill
        fields = ('id', 'skill', 'skill_name', 'category', 'proficiency_level', 'hourly_commitment', 'is_active', 'created_at')
        read_only_fields = ('user', 'created_at')


class LearnableSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    category = serializers.CharField(source='skill.category', read_only=True)

    class Meta:
        model = LearnableSkill
        fields = ('id', 'skill', 'skill_name', 'category', 'motivation', 'urgency', 'created_at')
        read_only_fields = ('user', 'created_at')
