from django.conf import settings
from django.db import models

class LeetCodeRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leetcode_records")
    problem_id = models.CharField(max_length=64)          # 如 1, 2, 3 或 slug
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    difficulty = models.CharField(max_length=16, choices=[("easy","easy"),("medium","medium"),("hard","hard")])
    status = models.CharField(max_length=16, choices=[("solved","solved"),("attempted","attempted")], default="solved")
    language = models.CharField(max_length=64, blank=True) # Python/Java/C++ 等
    tags = models.JSONField(default=list, blank=True)      # sqlite 可用 JSONField
    time_spent_min = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    solved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "problem_id")
        ordering = ["-solved_at", "-updated_at"]
