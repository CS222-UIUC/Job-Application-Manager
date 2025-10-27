from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="job.company.name", read_only=True)
    position = serializers.CharField(source="job.title", read_only=True)
    company_website = serializers.CharField(source="job.company.website", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "status",
            "applied_at",
            "created_at",
            "updated_at",
            "company_name",
            "position",
            "company_website",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
