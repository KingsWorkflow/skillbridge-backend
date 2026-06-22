from rest_framework import serializers
from .models import SkillExam, Question, ExamAttempt, SkillVerification


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id', 'text', 'question_type', 'options',
            'weight', 'explanation', 'order',
        )


class SkillExamSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    question_count = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = SkillExam
        fields = (
            'id', 'skill', 'skill_name', 'difficulty', 'difficulty_display',
            'title', 'time_limit_minutes', 'passing_score', 'questions',
            'question_count', 'total_weight', 'is_active', 'created_at',
        )
        read_only_fields = ('skill', 'is_active', 'created_at')

    def get_question_count(self, obj):
        return obj.questions.count()

    def get_questions(self, obj):
        qs = obj.questions.all().order_by('order')
        return QuestionSerializer(qs, many=True).data


class ExamAttemptSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='exam.skill.name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    total_weight = serializers.SerializerMethodField()
    earned_marks = serializers.SerializerMethodField()

    class Meta:
        model = ExamAttempt
        fields = (
            'id', 'user', 'exam', 'exam_title', 'skill_name',
            'score', 'passed', 'answers', 'started_at',
            'completed_at', 'can_retake_after', 'total_weight', 'earned_marks',
        )
        read_only_fields = ('user', 'started_at')

    def get_total_weight(self, obj):
        return obj.exam.total_weight

    def get_earned_marks(self, obj):
        if not obj.score:
            return 0
        return round((obj.score / 100) * obj.exam.total_weight, 2)


class SkillVerificationSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.category', read_only=True)
    level_label = serializers.SerializerMethodField()

    class Meta:
        model = SkillVerification
        fields = (
            'id', 'user', 'skill', 'skill_name', 'skill_category',
            'current_level', 'level_label', 'self_declared_at',
            'community_verified_at', 'certificate_verified_at',
            'platform_tested_at', 'expert_achieved_at',
            'verification_votes', 'total_teaching_hours', 'average_rating',
        )
        read_only_fields = ('user', 'self_declared_at')

    def get_level_label(self, obj):
        labels = {1: 'Self-declared', 2: 'Community rated', 3: 'Platform tested'}
        return labels.get(obj.current_level, 'Unverified')
