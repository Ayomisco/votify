from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, matriculation_number, email, password=None, **extra_fields):
        if matriculation_number is None:
            matriculation_number = ''  # Default to empty string if not provided
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(
            matriculation_number=matriculation_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(matriculation_number=None, email=email, password=password, **extra_fields)


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    matriculation_number = models.CharField(
        max_length=255, blank=True, null=True,  unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_superuser = models.BooleanField(
        default=False)  # Required for superuser access
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()


    class Meta:
        permissions = [
            ("can_view_dashboard", "Can view dashboard"),
            ("can_manage_users", "Can manage users"),
            ("can_edit_users", "Can edit users"),
            ("can_delete_users", "Can delete users"),
        ]


    def __str__(self):
        return f"{self.full_name} ({self.matriculation_number})"
