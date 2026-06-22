from django import forms


class ExamAnswerForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for q in questions:
            qid = q.get('id') if isinstance(q, dict) else getattr(q, 'id', None)
            label = q.get('text') if isinstance(q, dict) else getattr(q, 'text', '')
            field_name = f'question_{qid}'
            question_type = q.get('question_type') if isinstance(q, dict) else getattr(q, 'question_type', 'objective')

            if question_type == 'objective':
                options = q.get('options', []) if isinstance(q, dict) else getattr(q, 'options', [])
                self.fields[field_name] = forms.ChoiceField(
                    label=label,
                    choices=[(i, opt) for i, opt in enumerate(options)],
                    widget=forms.RadioSelect(attrs={'class': 'w-full'}),
                    required=True,
                )
            else:
                self.fields[field_name] = forms.CharField(
                    label=label,
                    widget=forms.Textarea(attrs={'class': 'w-full', 'rows': 3}),
                    required=True,
                )
