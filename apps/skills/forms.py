from django import forms
from .models import Skill, TeachableSkill, LearnableSkill


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('name', 'category', 'popularity_score')


class TeachableSkillForm(forms.ModelForm):
    class Meta:
        model = TeachableSkill
        fields = ('skill', 'proficiency_level', 'hourly_commitment')
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['skill'].queryset = Skill.objects.all()


class LearnableSkillForm(forms.ModelForm):
    class Meta:
        model = LearnableSkill
        fields = ('skill', 'motivation', 'urgency')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['skill'].queryset = Skill.objects.all()