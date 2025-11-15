from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    company_name = serializers.CharField(source="job.company.name", read_only=True)
    position = serializers.CharField(source="job.title", read_only=True)
    job_website = serializers.CharField(source="job.website", read_only=True)
    type = serializers.CharField(source="job.get_type_display", read_only=True)
    time = serializers.DateTimeField(source="applied_at", read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate(self, attrs):
        # do not ban
        if self.instance is None:
            request = self.context["request"]
            job = attrs.get("job")
            if job and Application.objects.filter(user=request.user, job=job).exists():
                raise serializers.ValidationError(
                    {"job": "You already created an application for this job."}
                )
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
