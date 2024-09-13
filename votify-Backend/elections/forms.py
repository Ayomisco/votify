from django import forms
from django.core.exceptions import ValidationError
from .models import Candidate


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'  # Use '__all__' to include all fields from the model

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
