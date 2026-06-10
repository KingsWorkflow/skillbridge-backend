from django import forms
from django.core.validators import MinValueValidator
from .models import Skill, TeachableSkill, LearnableSkill


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('name', 'category', 'popularity_score')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Python, React, Django',
                'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md',
            }),
            'category': forms.TextInput(attrs={
                'placeholder': 'e.g. Programming, Design, Marketing',
                'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md',
            }),
            'popularity_score': forms.NumberInput(attrs={
                'placeholder': '0.0 - 10.0',
                'min': '0',
                'max': '10',
                'step': '0.1',
                'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md',
            }),
        }


class TeachableSkillForm(forms.ModelForm):
    class Meta:
        model = TeachableSkill
        fields = ('skill', 'proficiency_level', 'hourly_commitment')
        widgets = {
            'proficiency_level': forms.Select(attrs={
                'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md',
            }),
            'hourly_commitment': forms.NumberInput(attrs={
                'placeholder': 'Hours per week',
                'min': '1',
                'max': '40',
                'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['skill'].queryset = Skill.objects.all()
        self.fields['skill'].empty_label = "Select a skill"
        self.fields['skill'].widget.attrs.update({
            'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md',
        })

    def clean_hourly_commitment(self):
        hours = self.cleaned_data.get('hourly_commitment')
        if hours is not None and (hours < 1 or hours > 40):
            raise forms.ValidationError('Commitment must be between 1 and 40 hours per week.')
        return hours


class LearnableSkillForm(forms.ModelForm):
    motivation = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'placeholder': 'Why do you want to learn this skill?',
            'rows': 3,
            'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md',
        })
    )

    class Meta:
        model = LearnableSkill
        fields = ('skill', 'motivation', 'urgency')
        widgets = {
            'urgency': forms.Select(attrs={
                'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['skill'].queryset = Skill.objects.all()
        self.fields['skill'].empty_label = "Select a skill"
        self.fields['skill'].widget.attrs.update({
            'class': 'w-full px-sm py-base border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary font-body-md',
        })
