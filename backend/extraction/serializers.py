from rest_framework import serializers


class ExtractRequestSerializer(serializers.Serializer):
    url = serializers.URLField()


class ExtractResponseSerializer(serializers.Serializer):
    url = serializers.URLField()
    text = serializers.CharField()
    chars = serializers.IntegerField()
    cached = serializers.BooleanField()
