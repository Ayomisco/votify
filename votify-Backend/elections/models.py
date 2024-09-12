from django.db import models
from django.conf import settings
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Election(models.Model):
    GENERAL = 'General'
    DEPARTMENT = 'Department'
    COURSE = 'Course'

    ELECTION_TYPE_CHOICES = [
        (GENERAL, 'General Election'),
        (DEPARTMENT, 'Department Election'),
        (COURSE, 'Course Election'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Upcoming', 'Upcoming'),
        ('Finished', 'Finished'),
    ]

    title = models.CharField(max_length=255)
    election_type = models.CharField(
        max_length=20,
        choices=ELECTION_TYPE_CHOICES,
        default=GENERAL
    )
    department = models.CharField(
        max_length=100,
        choices=[
            ('Marine Engineering', 'Marine Engineering'),
            ('Nautical Science', 'Nautical Science'),
            ('Maritime Transport and Business Studies',
             'Maritime Transport and Business Studies'),
            ('Computer Science', 'Computer Science'),
            ('Fisheries Technology', 'Fisheries Technology'),
            ('Mechanical Engineering', 'Mechanical Engineering'),
            ('Science Laboratory Technology', 'Science Laboratory Technology'),
            ('Industrial and Labour Relations', 'Industrial and Labour Relations'),
            ('Oceanography and Fisheries Science',
             'Oceanography and Fisheries Science'),
            ('Hydrology and Water Resources Management',
             'Hydrology and Water Resources Management'),
        ],
        null=True,
        blank=True
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Upcoming'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.end_date < timezone.now():
            self.status = 'Finished'
        elif self.start_date <= timezone.now() <= self.end_date:
            self.status = 'Active'
        else:
            self.status = 'Upcoming'
        super().save(*args, **kwargs)

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
    department = models.CharField(
        max_length=100,
        choices=[
            ('Marine Engineering', 'Marine Engineering'),
            ('Nautical Science', 'Nautical Science'),
            ('Maritime Transport and Business Studies',
             'Maritime Transport and Business Studies'),
            ('Computer Science', 'Computer Science'),
            ('Fisheries Technology', 'Fisheries Technology'),
            ('Mechanical Engineering', 'Mechanical Engineering'),
            ('Science Laboratory Technology', 'Science Laboratory Technology'),
            ('Industrial and Labour Relations', 'Industrial and Labour Relations'),
            ('Oceanography and Fisheries Science',
             'Oceanography and Fisheries Science'),
            ('Hydrology and Water Resources Management',
             'Hydrology and Water Resources Management'),
        ],
        null=True,
        blank=True
    )
    school_level = models.CharField(
        max_length=10,
        choices=SCHOOL_LEVEL_CHOICES
    )
    position = models.CharField(max_length=255)
    about = models.TextField()
    manifesto = models.TextField()
    image = CloudinaryField('candidate/image', null=True, blank=True)

    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    votes_count = models.PositiveIntegerField(default=0)
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


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'election')
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

    def __str__(self):
        return f"{self.user} voted for {self.candidate} in {self.election}"
