from django.db import models
from users.models import Department  # Importing Department from users.models


class Election(models.Model):
    GENERAL = 'General'
    DEPARTMENT = 'Department'
    COURSES = 'Courses'

    ELECTION_TYPE_CHOICES = [
        ('General', 'General Election'),
        ('Department', 'Department Election'),
        ('Course', 'Course Election'),
    ]

    title = models.CharField(max_length=255)
    election_type = models.CharField(
        max_length=20,
        choices=ELECTION_TYPE_CHOICES,
        default=GENERAL
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Optional for general elections.'
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Election'
        verbose_name_plural = 'Elections'


class Candidate(models.Model):
    ND1 = 'ND1'
    ND2 = 'ND2'
    HNG1 = 'HNG1'
    HNG2 = 'HNG2'

    SCHOOL_LEVEL_CHOICES = [
        (ND1, 'ND1'),
        (ND2, 'ND2'),
        (HNG1, 'HNG1'),
        (HNG2, 'HNG2'),
    ]

    full_name = models.CharField(max_length=255)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        help_text='The department the candidate belongs to.'
    )
    school_level = models.CharField(
        max_length=10,
        choices=SCHOOL_LEVEL_CHOICES
    )
    position = models.CharField(max_length=255)
    about = models.TextField()
    manifesto = models.TextField()
    image = models.ImageField(
        upload_to='candidates/images/',
        null=True,
        blank=True
    )
    course_studying = models.CharField(max_length=255)
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} for {self.position}"

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
        indexes = [
            models.Index(fields=['election']),
        ]
