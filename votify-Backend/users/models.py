from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils import timezone


import re
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, matriculation_number='', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not full_name:
            raise ValueError('The Full Name field must be set')

        # Validate email format
        self.validate_email_format(email)

        # Normalize email
        email = self.normalize_email(email)

        user = self.model(
            matriculation_number=matriculation_number, full_name=full_name, email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email=email, full_name=full_name, password=password, **extra_fields)

    def validate_email_format(self, email):
        """Ensure email is in the format name.surname@fcfmt.edu.ng."""
        email_regex = r'^[a-zA-Z]+\.[a-zA-Z]+@fcfmt\.edu\.ng$'
        if not re.match(email_regex, email):
            raise ValidationError(
                'Invalid email format. Email must be in the format name.surname@fcfmt.edu.ng'
            )


class User(AbstractBaseUser, PermissionsMixin):
    ND1 = 'ND1'
    ND2 = 'ND2'
    HNG1 = 'HND1'
    HNG2 = 'HND2'

    SCHOOL_LEVEL_CHOICES = [
        (ND1, 'ND1'),
        (ND2, 'ND2'),
        (HNG1, 'HND1'),
        (HNG2, 'HND2'),
    ]

    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]


# Department choices
    MARINE_ENGINEERING = 'Marine Engineering'
    NAUTICAL_SCIENCE = 'Nautical Science'
    MARITIME_TRANSPORT = 'Maritime Transport and Business Studies'
    COMPUTER_SCIENCE = 'Computer Science'
    FISHERIES_TECHNOLOGY = 'Fisheries Technology'
    MECHANICAL_ENGINEERING = 'Mechanical Engineering'
    LAB_TECHNOLOGY = 'Science Laboratory Technology'
    LABOUR_RELATIONS = 'Industrial and Labour Relations'
    OCEANOGRAPHY = 'Oceanography and Fisheries Science'
    HYDROLOGY = 'Hydrology and Water Resources Management'

    DEPARTMENT_CHOICES = [
        (MARINE_ENGINEERING, 'Marine Engineering'),
        (NAUTICAL_SCIENCE, 'Nautical Science'),
        (MARITIME_TRANSPORT, 'Maritime Transport and Business Studies'),
        (COMPUTER_SCIENCE, 'Computer Science'),
        (FISHERIES_TECHNOLOGY, 'Fisheries Technology'),
        (MECHANICAL_ENGINEERING, 'Mechanical Engineering'),
        (LAB_TECHNOLOGY, 'Science Laboratory Technology'),
        (LABOUR_RELATIONS, 'Industrial and Labour Relations'),
        (OCEANOGRAPHY, 'Oceanography and Fisheries Science'),
        (HYDROLOGY, 'Hydrology and Water Resources Management'),
    ]


    department = models.CharField(
        max_length=100, choices=DEPARTMENT_CHOICES, null=True, blank=True
    )

    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default='student')

    
    matriculation_number = models.CharField(
        max_length=255, blank=True, null=True,  unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
   # Use the choices for departments
    department = models.CharField(
        max_length=100, choices=DEPARTMENT_CHOICES, null=True, blank=True
    )
    school_level = models.CharField(
        max_length=10,
        choices=SCHOOL_LEVEL_CHOICES, null=True, blank=True
    )
    profile_pic = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_superuser = models.BooleanField(
        default=False)  # Required for superuser access
    is_active = models.BooleanField(default=True)  # Required for admin access

    

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

        # Orders by 'created_at' descending, then by 'full_name' ascending
        ordering = ['-created_at', 'full_name']

    


    def __str__(self):
        return f"{self.full_name} ({self.matriculation_number})"
