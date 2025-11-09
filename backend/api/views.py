from django.conf import settings
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Item
from .serializers import ChatMessageSerializer, ItemSerializer

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by("-id")
    serializer_class = ItemSerializer


class ItemRetrieveView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def chat(request):
    """Chat with OpenAI API"""
    if not OpenAI:
        return Response(
            {"error": "OpenAI library is not installed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    serializer = ChatMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    message = serializer.validated_data["message"]
    conversation_history = serializer.validated_data.get("conversation_history", [])

    # 获取OpenAI API key
    api_key = getattr(settings, "OPENAI_API_KEY", None)
    if not api_key:
        return Response(
            {"error": "OpenAI API key is not configured. Please set OPENAI_API_KEY in your environment variables or .env file."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        client = OpenAI(api_key=api_key)

        messages = []
        messages.append(
            {
                "role": "system",
                "content": "You are a helpful AI assistant for a job application tracking system. Help users with job search, resume advice, interview preparation, and career guidance.",
            }
        )

        for msg in conversation_history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, temperature=0.7, max_tokens=1000
        )

        ai_response = response.choices[0].message.content

        return Response({"response": ai_response}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Failed to get AI response: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
