from django import forms
from .models import Certificate, SkillExam
from apps.skills.models import Skill


class CertificateUploadForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('skill', 'certificate_file', 'issuing_organization', 'certificate_id', 'issue_date')


class ExamAnswerForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, question in enumerate(questions):
            self.fields[f'question_{i}'] = forms.CharField(
                widget=forms.TextInput(attrs={'class': 'w-full'}),
                required=True
            )


class SkillSelectionForm(forms.Form):
    skill = forms.ChoiceField(widget=forms.Select(attrs={'class': 'w-full'}))
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['skill'].choices = [
                (skill.id, skill.name) 
                for skill in Skill.objects.all()
            ]