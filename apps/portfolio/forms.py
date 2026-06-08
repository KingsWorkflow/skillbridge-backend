from django import forms
from .models import Project, Certification as PortfolioCertification


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'project_url', 'image')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full'}),
        }


class PortfolioCertificationForm(forms.ModelForm):
    class Meta:
        model = PortfolioCertification
        fields = ('name', 'issuing_organization', 'issue_date', 'certificate_file', 'verification_url')