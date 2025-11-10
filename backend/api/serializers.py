from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "title", "content", "created_at", "updated_at"]


class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, allow_blank=False)
    conversation_history = serializers.ListField(
        child=serializers.DictField(), required=False, allow_empty=True
    )
