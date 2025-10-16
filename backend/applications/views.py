from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Application
from .serializers import ApplicationSerializer

@api_view(['GET'])
def get_applications(request):
    apps = Application.objects.all()
    serializer = ApplicationSerializer(apps, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_application(request):
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)