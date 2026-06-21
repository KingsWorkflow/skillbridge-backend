from django import forms
from apps.skills.models import TeachableSkill, LearnableSkill
from .models import ExchangeProposal, ExchangeSession


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ('offer_skill', 'request_skill', 'proposed_hours', 'message')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        receiver = kwargs.pop('receiver', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['offer_skill'].queryset = TeachableSkill.objects.filter(
                user=user, is_active=True
            ).select_related('skill')
        if receiver is not None:
            self.fields['request_skill'].queryset = LearnableSkill.objects.filter(
                user=receiver
            ).select_related('skill')


class ExchangeSessionForm(forms.ModelForm):
    scheduled_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    class Meta:
        model = ExchangeSession
        fields = ('scheduled_date', 'duration_hours', 'meeting_link', 'notes')
        widgets = {
            'duration_hours': forms.NumberInput(attrs={'min': 1}),
        }


class SessionRatingForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=5,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5})
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )