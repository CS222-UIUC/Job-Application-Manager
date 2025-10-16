from django.contrib import admin
from .models import Company, Job, Application


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'created_at')
    search_fields = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'created_at')
    search_fields = ('title',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'status', 'applied_at', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'job__title', 'job__company__name']
    autocomplete_fields = ['user', 'job']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'job', 'job__company')