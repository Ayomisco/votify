# users/forms.py
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Department
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model




class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'department')


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['matriculation_number', 'full_name',
                  'department', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate department choices
        self.fields['department'].queryset = Department.objects.all()

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'department', 'profile_pic',
                   'is_staff', 'is_superuser')

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Matriculation Number", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def confirm_login_allowed(self, user):
        if not user.matriculation_number:
            raise forms.ValidationError(
                "This user does not have a matriculation number.",
                code='no_matriculation_number',
            )
        super().confirm_login_allowed(user)


class AdminLoginForm(AuthenticationForm):
    email = forms.EmailField(label="Email" ,)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def confirm_login_allowed(self, user):
        if user.matriculation_number:
            raise forms.ValidationError(
                "Admins should log in using their email.",
                code='email_required',
            )
        super().confirm_login_allowed(user)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password.")

        return cleaned_data




class CustomAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()  # Use the user model dynamically
        # Remove 'confirm_password'
        fields = ['email', 'full_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Email address is already in use.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
