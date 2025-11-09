from rest_framework import serializers

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=4000)
    stream = serializers.BooleanField(required=False, default=False)

class ChatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()