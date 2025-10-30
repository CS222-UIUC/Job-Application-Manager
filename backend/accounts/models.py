from django.contrib.auth.models import User
from django.db import models


def resume_path(instance, filename):
    return f"resumes/user_{instance.user_id}/{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    resume = models.FileField(upload_to=resume_path, null=True, blank=True)
    resume_uploaded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
