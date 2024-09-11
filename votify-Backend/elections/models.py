from django.db import models


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
