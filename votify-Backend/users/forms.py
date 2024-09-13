import logging
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User

# Set up logging
logger = logging.getLogger(__name__)

# Custom User Change Form


class CustomUserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'department', 'profile_pic', 'user_type',
                  'is_staff', 'is_superuser', 'school_level', 'matriculation_number',)



class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    school_level = forms.ChoiceField(
        choices=User.SCHOOL_LEVEL_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['matriculation_number', 'school_level',
                  'full_name', 'department', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # Department choices are directly from the User model
            self.fields['department'].choices = User.DEPARTMENT_CHOICES
            logger.debug(f"Department choices set to: {User.DEPARTMENT_CHOICES}")

        except Exception as e:
            logger.error(f"Error loading departments: {e}")
            raise ValidationError(
                "Error loading departments. Please try again later.")



    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        try:
            if password and confirm_password and password != confirm_password:
                raise ValidationError("Passwords do not match")

            matriculation_number = cleaned_data.get('matriculation_number')
            if matriculation_number:
                matriculation_number = matriculation_number.strip().lower()
                if User.objects.filter(matriculation_number__iexact=matriculation_number).exists():
                    raise ValidationError(
                        "Matriculation number is already in use.")

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in form cleaning: {e}")
            raise ValidationError(
                "An unexpected error occurred. Please try again later.")

        return cleaned_data

    def save(self, commit=True):
        try:
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password'])
            user.user_type = 'student'  # Set default user type to 'student'
            if commit:
                user.save()
            logger.info(f"User created successfully: {user}")
            return user
        except Exception as e:
            logger.error(f"Error saving user: {e}")
            raise ValidationError(
                "An error occurred while saving the user. Please try again later.")

# Custom Admin Creation Form


class CustomAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()  # Dynamically reference the user model
        fields = ['email', 'full_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        try:
            if password and confirm_password and password != confirm_password:
                raise ValidationError("Passwords do not match")
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in admin form cleaning: {e}")
            raise ValidationError(
                "An unexpected error occurred. Please try again later.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            if get_user_model().objects.filter(email=email).exists():
                raise ValidationError("Email address is already in use.")
        except Exception as e:
            logger.error(f"Error checking email uniqueness: {e}")
            raise ValidationError("An error occurred. Please try again later.")
        return email

    def save(self, commit=True):
        try:
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password'])
            user.user_type = 'admin'  # Set default user type to 'admin'
            if commit:
                user.save()
            logger.info(f"Admin user created successfully: {user}")
            return user
        except Exception as e:
            logger.error(f"Error saving admin user: {e}")
            raise ValidationError(
                "An error occurred while saving the admin. Please try again later.")

# Custom Login Form for Students


class CustomLoginForm(AuthenticationForm):
    matriculation_number = forms.CharField(
         max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        matriculation_number = cleaned_data.get('matriculation_number')
        password = cleaned_data.get('password')

        try:
            if matriculation_number and password:
                user = authenticate(
                    matriculation_number=matriculation_number, password=password)
                if user is None:
                    raise ValidationError(
                        "Invalid matriculation number or password.")
        except ValidationError as e:
            logger.error(f"Validation error during login: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during student login: {e}")
            raise ValidationError(
                "An unexpected error occurred during login. Please try again later.")

        return cleaned_data


    

# Custom Login Form for Admins


class AdminLoginForm(AuthenticationForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        try:
            if email and password:
                user = authenticate(request=self.request,
                                    username=email, password=password)
                if user is None:
                    raise ValidationError(
                        "Invalid email or password, or you do not have permission to access the admin.")
                elif not user.is_staff:
                    raise ValidationError(
                        "You do not have permission to access the admin.")
        except ValidationError as e:
            logger.error(f"Validation error during admin login: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during admin login: {e}")
            raise ValidationError(
                "An unexpected error occurred during login. Please try again later.")

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'matriculation_number',
                  'department', 'school_level', 'profile_pic']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'matriculation_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'school_level': forms.Select(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }
