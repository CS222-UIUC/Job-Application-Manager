from rest_framework import serializers

from .models import LeetCodeProblem, UserProblemRecord


class LeetCodeProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeetCodeProblem
        fields = ["problem_id", "title", "difficulty", "tags", "url"]


class UserProblemRecordSerializer(serializers.ModelSerializer):
    problem = LeetCodeProblemSerializer(read_only=True)
    problem_id = serializers.PrimaryKeyRelatedField(
        queryset=LeetCodeProblem.objects.all(),
        source="problem",
        write_only=True,
    )

    class Meta:
        model = UserProblemRecord
        fields = ["problem", "problem_id", "solved_at"]

    def create(self, validated_data):
        return super().create(validated_data)
