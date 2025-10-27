from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application, JobApplication
from .serializers import ApplicationSerializer, JobApplicationSerializer


@api_view(["GET"])
def get_applications(request):
    u = request.user
    qs = Application.objects.all() if (u.is_staff or u.is_superuser) else Application.objects.filter(user=u)
    data = ApplicationSerializer(qs, many=True).data
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_application(request):
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# new version, add the authentication check
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_job_applications(request):
    apps = JobApplication.objects.filter(user=request.user)
    serializer = JobApplicationSerializer(apps, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_job_application(request):
    serializer = JobApplicationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
