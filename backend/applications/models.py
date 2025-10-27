from django.db import models
from django.conf import settings


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      # updated time
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
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, 
        related_name='jobs', 
    )
    title = models.CharField(max_length=150)
    class Meta:
        unique_together = [('company', 'title')] 
    def __str__(self):
        return f'{self.title} @ {self.company}'



class Application(TimeStamped):
    class Status(models.TextChoices):
        STARTED = "started", "Started"
        OA = "oa", "Online Assessment"
        INTERVIEW = "interview", "Interview"
        OFFERED = "offered", "Offered"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.STARTED)
    applied_at = models.DateTimeField(null=True, blank=True)
    deadline_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [('user', 'job')]
        indexes = [
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"{self.user} → {self.job} ({self.status})"


# new version, match the frontend data format
class JobApplication(TimeStamped):
    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        OA = "oa", "OA"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    class Type(models.TextChoices):
        FULLTIME = "fulltime", "Full Time"
        INTERN = "intern", "Intern"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_applications"
    )
    company = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    link = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.FULLTIME)
    time = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)

    class Meta:
        unique_together = [("user", "company", "position")]
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"{self.user} → {self.company} - {self.position} ({self.status})"
