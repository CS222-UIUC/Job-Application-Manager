from django.contrib import admin
from .models import LeetCodeRecord
@admin.register(LeetCodeRecord)
class LeetCodeRecordAdmin(admin.ModelAdmin):
    list_display = ("user","problem_id","title","difficulty","status","solved_at","updated_at")
    search_fields = ("title","problem_id","user__username")
    list_filter = ("difficulty","status")