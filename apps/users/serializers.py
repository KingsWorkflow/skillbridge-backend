from rest_framework import serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'phone', 'bio', 'profile_picture', 
                  'experience_level', 'skill_credits', 'beginner_tokens', 
                  'reputation_score', 'total_hours_taught', 'total_hours_learned']
        read_only_fields = ['skill_credits', 'beginner_tokens', 'reputation_score', 
                           'total_hours_taught', 'total_hours_learned']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user