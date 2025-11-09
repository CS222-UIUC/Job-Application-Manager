# backend/ai/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
@permission_classes([AllowAny])   
def chat(request):
    msg = request.data.get("message", "")
    return Response({"reply": f"[stub] You said: {msg}"}, status=status.HTTP_200_OK)
