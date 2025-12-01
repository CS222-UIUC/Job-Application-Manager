# backend/leetcode/serializers.py
from rest_framework import serializers
from .models import Problem, Submission, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id","name"]

class ProblemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Problem
        fields = ["id","number","slug","title","difficulty","url","tags","updated_at"]

class ProblemCreateSerializer(serializers.ModelSerializer):
    tag_names = serializers.ListField(child=serializers.CharField(), required=False, default=[])
    class Meta:
        model = Problem
        fields = ["number","slug","title","difficulty","url","tag_names"]
    def create(self, validated):
        tags = validated.pop("tag_names", [])
        p = Problem.objects.create(**validated)
        if tags:
            objs = [Tag.objects.get_or_create(name=t.strip())[0] for t in tags]
            p.tags.set(objs)
        return p

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        read_only_fields = ["user", "submitted_at"]
        fields = ["id","problem","status","language","runtime_ms","memory_kb","code","submitted_at"]
    def create(self, validated):
        validated["user"] = self.context["request"].user
        return super().create(validated)
