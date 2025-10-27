# backend/applications/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer
# Prevent duplicate applications and enforce authenticated user binding
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_applications(request):
    u = request.user
    qs = Application.objects.all() if (u.is_staff or u.is_superuser) else Application.objects.filter(user=u)
    data = ApplicationSerializer(qs, many=True).data
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_application(request):
    serializer = ApplicationSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)      
    serializer.save()                             
    return Response(serializer.data, status=201)
