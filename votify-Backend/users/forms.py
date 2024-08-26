from .models import User, Department
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate




class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'department')


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    school_level = forms.ChoiceField(
        choices=User.SCHOOL_LEVEL_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['matriculation_number', 'school_level', 'full_name',
                  'department', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate department choices
        self.fields['department'].queryset = Department.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        matriculation_number = cleaned_data.get('matriculation_number')
        if matriculation_number:
            matriculation_number = matriculation_number.strip().lower()
            print(f"Checking if matriculation number {
                matriculation_number} exists.")

            if User.objects.filter(matriculation_number__iexact=matriculation_number).exists():
                print(f"Matriculation number {
                    matriculation_number} is already in use.")
                raise forms.ValidationError(
                    "Matriculation number is already in use.")

        return cleaned_data



    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            print("Saving user:", user)

            user.save()
        return user



class CustomUserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'department', 'profile_pic',
                  'is_staff', 'is_superuser', 'school_level', 'matriculation_number', )

class CustomLoginForm(AuthenticationForm):

    matriculation_number = forms.CharField(
        label="Matriculation Number", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        matriculation_number = cleaned_data.get('matriculation_number')
        password = cleaned_data.get('password')

        if matriculation_number and password:
            user = authenticate(
                matriculation_number=matriculation_number, password=password)
            if user is None:
                raise forms.ValidationError(
                    "Invalid matriculation number or password.")
        return cleaned_data


class AdminLoginForm(AuthenticationForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


    '''
    def confirm_login_allowed(self, user):
        if user.email:
            raise forms.ValidationError(
                "Admins should log in using their email.",
                code='email_required',
            )
        super().confirm_login_allowed(user)'''


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None or not user.is_staff:
                raise forms.ValidationError(
                    "Invalid email or password, or you do not have permission to access the admin.")
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
