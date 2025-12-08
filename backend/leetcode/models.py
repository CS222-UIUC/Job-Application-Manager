from django.conf import settings
from django.db import models


class LeetCodeProblem(models.Model):
    """
    Problem Info
    """

    problem_id = models.PositiveIntegerField(primary_key=True)  # LeetCode problem ID
    title = models.CharField(max_length=255)  # problem title
    difficulty = models.CharField(
        max_length=10,
        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
    )
    tags = models.JSONField(default=list, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.difficulty})"


class UserProblemRecord(models.Model):
    """
    User's record for a specific problem
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leetcode_records",
    )
    problem = models.ForeignKey(
        LeetCodeProblem,
        on_delete=models.CASCADE,
        related_name="user_records",
    )

    solved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "problem")

    def __str__(self):
        return f"{self.user} - {self.problem}"
