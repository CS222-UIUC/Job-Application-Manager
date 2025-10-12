from django.contrib import admin
from .models import Company, Job

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'created_at')
    search_fields = ('name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title',)