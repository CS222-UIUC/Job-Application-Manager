from django.contrib import admin

from .models import LeetCodeProblem, UserProblemRecord


@admin.register(LeetCodeProblem)
class LeetCodeProblemAdmin(admin.ModelAdmin):
    list_display = ("problem_id", "title", "difficulty", "url", "tag_list")
    list_filter = ("difficulty",)
    search_fields = ("title", "problem_id", "url")
    ordering = ("problem_id",)

    def tag_list(self, obj):
        return ", ".join(obj.tags or [])

    tag_list.short_description = "Tags"


@admin.register(UserProblemRecord)
class UserProblemRecordAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "problem",
        "solved_at",
    )
    list_filter = ("problem__difficulty",)
    search_fields = (
        "user__username",
        "problem__title",
        "problem__problem_id",
    )
    autocomplete_fields = ("user", "problem")
