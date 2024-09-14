# forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Candidate, Election, Vote


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'  # Include all fields from the model

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check if the file is an image
            if not image.content_type.startswith('image/'):
                raise ValidationError("The file must be an image.")

            # Check the image size (for example, less than 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if image.size > max_size:
                raise ValidationError(
                    "The image file size must be less than 5MB.")
        return image


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(
                "End date must be after the start date.")
        return cleaned_data


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['candidate', 'election']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        candidate = cleaned_data.get("candidate")
        election = cleaned_data.get("election")

        if self.user and candidate and election:
            if candidate.user != self.user:
                raise forms.ValidationError("You can only vote for yourself.")
            if Vote.objects.filter(user=self.user, election=election).exists():
                raise forms.ValidationError(
                    "You have already voted in this election.")
        return cleaned_data
