from django.conf import settings
from django.db import models


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # created time
    updated_at = models.DateTimeField(auto_now=True)  # last updated time

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
        on_delete=models.CASCADE,  # when company deleted, delete all its jobs
        related_name="jobs",  # company.jobs to access all jobs of a company
    )
    title = models.CharField(max_length=150)

    class Meta:
        unique_together = [("company", "title")]  # same company can't have duplicate job titles

    def __str__(self):
        return f"{self.title} @ {self.company}"


# application chart (user's application to a job)
class Application(TimeStamped):
    class Status(models.TextChoices):
        STARTED = "started", "Started"
        OA = "oa", "Online Assessment"
        INTERVIEW = "interview", "Interview"
        OFFERED = "offered", "Offered"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.STARTED)
    applied_at = models.DateTimeField(null=True, blank=True)
    deadline_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("user", "job")]
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"{self.user} → {self.job} ({self.status})"
