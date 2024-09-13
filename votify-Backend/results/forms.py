# results/forms.py

from django import forms
from .models import Winner, Result
from elections.models import Candidate


class WinnerForm(forms.ModelForm):
    class Meta:
        model = Winner
        fields = ['result', 'candidate', 'announced_at']
        widgets = {
            'announced_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'result' in self.data:
            try:
                result = Result.objects.get(pk=self.data.get('result'))
                winners = result.get_winner()
                if winners:
                    # Set the queryset for candidates
                    self.fields['candidate'].queryset = Candidate.objects.filter(
                        pk__in=[winner.pk for winner in winners])
                    if not self.instance.pk:
                        # Automatically select the winner with highest votes
                        self.instance.candidate = winners[0]
                        # Set candidate field to read-only
                        self.fields['candidate'].widget.attrs['readonly'] = True
            except (ValueError, TypeError, Result.DoesNotExist):
                pass

    def clean(self):
        cleaned_data = super().clean()
        result = cleaned_data.get('result')
        if result and not self.instance.pk:
            winners = result.get_winner()
            if winners:
                self.instance.candidate = winners[0]
        return cleaned_data
