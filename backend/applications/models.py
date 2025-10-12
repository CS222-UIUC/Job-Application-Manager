from django.db import models

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # created time
    updated_at = models.DateTimeField(auto_now=True)      # last updated time
    class Meta:
        abstract = True

# company chart
class Company(TimeStamped):
    name = models.CharField(max_length=150, unique=True)
    website = models.URLField(blank=True)
    def __str__(self):
        return self.name

# job chart
class Job(TimeStamped):
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('oa', 'Online Assessment'),
        ('Interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, # when company deleted, delete all its jobs
        related_name='jobs', # company.jobs to access all jobs of a company
    )
    title = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='started')

    class Meta:
        indexes = [models.Index(fields=['status'])] # index for filtering jobs by status
        unique_together = [('company', 'title')] # same company can't have duplicate job titles

    def __str__(self):
        return f'{self.title} @ {self.company}'