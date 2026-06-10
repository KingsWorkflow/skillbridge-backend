from django.urls import path
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Skill, TeachableSkill, LearnableSkill
from .serializers import SkillSerializer, TeachableSkillSerializer, LearnableSkillSerializer


app_name = 'skills_api'


class SkillListAPIView(APIView):
    def get(self, request):
        q = request.GET.get('q', '').strip()
        category = request.GET.get('category', '').strip()
        skills = Skill.objects.all()
        if q:
            skills = skills.filter(name__icontains=q)
        if category:
            skills = skills.filter(category__iexact=category)
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)


class TeachableSkillListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teachable = TeachableSkill.objects.filter(user=request.user, is_active=True).select_related('skill')
        serializer = TeachableSkillSerializer(teachable, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeachableSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeachableSkillDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        skill = TeachableSkill.objects.filter(pk=pk, user=request.user).first()
        if not skill:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LearnableSkillListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        learnable = LearnableSkill.objects.filter(user=request.user).select_related('skill')
        serializer = LearnableSkillSerializer(learnable, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LearnableSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LearnableSkillDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        skill = LearnableSkill.objects.filter(pk=pk, user=request.user).first()
        if not skill:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


urlpatterns = [
    path('skills/', SkillListAPIView.as_view(), name='skill_list'),
    path('teachable/', TeachableSkillListAPIView.as_view(), name='teachable_list'),
    path('teachable/<int:pk>/', TeachableSkillDetailAPIView.as_view(), name='teachable_detail'),
    path('learnable/', LearnableSkillListAPIView.as_view(), name='learnable_list'),
    path('learnable/<int:pk>/', LearnableSkillDetailAPIView.as_view(), name='learnable_detail'),
]
