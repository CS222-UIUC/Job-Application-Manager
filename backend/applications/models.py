from django.conf import settings
from django.db import models


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # updated time

    class Meta:
        abstract = True


# company chart
class Company(TimeStamped):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


# job chart
class Job(TimeStamped):
    class Status(models.TextChoices):
        FULL_TIME = "full_time", "Full Time"
        INTERN = "intern", "Intern"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    title = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=Status.choices, default=Status.FULL_TIME)
    website = models.URLField(blank=True)

    class Meta:
        unique_together = [("company", "title")]

    def __str__(self):
        return f"{self.title} @ {self.company}"


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

    class Meta:
        unique_together = [("user", "job")]
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"{self.user} → {self.job} ({self.status})"
