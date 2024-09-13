from django.db import models
from django.conf import settings
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Election(models.Model):
    PRESIDENT = 'The president'
    VICE_PRESIDENT = 'The vp'
    TREASURER = 'The treasurer'
    PRO = 'The Pro'
    GENERAL_SECRETARY = 'The General secretary'
    FINANCIAL_SECRETARY = 'The Financial Secretary'
    WELFARE_OFFICER = 'The Welfare Officer'
    ASSISTANT_GENERAL_SECRETARY = 'The assistant General secretary'

    ELECTION_TYPE_CHOICES = [
        (PRESIDENT, 'Presidential Election'),
        (VICE_PRESIDENT, 'Vice President Election'),
        (TREASURER, 'Treasurer Election'),
        (PRO, 'PRO Election'),
        (GENERAL_SECRETARY, 'General Secretary Election'),
        (FINANCIAL_SECRETARY, 'Financial Secretary Election'),
        (WELFARE_OFFICER, 'Welfare Officer Election'),
        (ASSISTANT_GENERAL_SECRETARY, 'Assistant General Secretary Election'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Upcoming', 'Upcoming'),
        ('Finished', 'Finished'),
    ]

    election_type = models.CharField(
        max_length=200,
        choices=ELECTION_TYPE_CHOICES,
        default=PRESIDENT
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
        return self.election_type

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
        verbose_name_plural = '     Elections'

class Candidate(models.Model):
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
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    matriculation_number = models.CharField(
        max_length=255, blank=True, null=True,  unique=True)
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
    about = models.TextField()
    manifesto = models.TextField()
    image = CloudinaryField('candidate/image', null=True, blank=True)

    votes_count = models.PositiveIntegerField(
        default=0)  # Track votes per candidate

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} for {self.election}"



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
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'election')
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

    def __str__(self):
        return f"{self.user} voted for {self.candidate} in {self.election}"

    # Track today's votes for an election
    @classmethod
    def today_votes(cls, election):
        today = timezone.now().date()
        return cls.objects.filter(election=election, voted_at__date=today).count()
