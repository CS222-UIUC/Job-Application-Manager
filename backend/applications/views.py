from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application, Company, Job
from .serializers import ApplicationSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_applications(request):
    apps = Application.objects.filter(user=request.user)
    serializer = ApplicationSerializer(apps, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_application(request):
    try:
        # get or create company
        company, _ = Company.objects.get_or_create(name=request.data.get("company"))

        # get or create job
        job, _ = Job.objects.get_or_create(
            company=company,
            title=request.data.get("position"),
            defaults={"website": request.data.get("link", "")},
        )

        # create application
        application = Application.objects.create(
            user=request.user,
            job=job,
            status=request.data.get("status", "applied"),
            applied_at=request.data.get("time"),
        )

        # prepare data to return to frontend using serializer for consistency
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {"error": str(e), "message": "Failed to create application"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_application(request, pk):
    try:
        application = Application.objects.get(pk=pk, user=request.user)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Application.DoesNotExist:
        return Response(
            {"error": "Application not found or you don't have permission to delete it"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"error": str(e), "message": "Failed to delete application"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
