from rest_framework import serializers


class ExtractRequestSerializer(serializers.Serializer):
    url = serializers.URLField()


class ExtractResponseSerializer(serializers.Serializer):
    url = serializers.URLField()
    text = serializers.CharField()
    chars = serializers.IntegerField()


class SkillCategory(serializers.Serializer):
    name = serializers.CharField()
    skills = serializers.ListField(child=serializers.CharField())


class SkillExtractGenericResp(serializers.Serializer):
    url = serializers.URLField()
    categories = SkillCategory(many=True)
    flat = serializers.ListField(child=serializers.CharField())
    jd_chars = serializers.IntegerField()
