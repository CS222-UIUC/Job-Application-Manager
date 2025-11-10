from django.contrib.auth import login, logout
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import (
    PasswordChangeSerializer,
    ResumeSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """user registration"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "token": token.key,
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    """user login"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response(
            {"user": UserSerializer(user).data, "token": token.key, "message": "Login successful"}
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """user logout"""
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    logout(request)
    return Response({"message": "Logout successful"})


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """get/update user profile"""
    if request.method == "GET":
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data, "message": "Profile updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    """change password"""
    serializer = PasswordChangeSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({"message": "Password changed successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """delete account"""
    user = request.user
    user.delete()
    return Response({"message": "Account deleted successfully"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_auth(request):
    """check user authentication status"""
    return Response({"authenticated": True, "user": UserSerializer(request.user).data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_resume(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return Response(
        {
            "has_resume": bool(profile.resume),
            "resume_url": (
                request.build_absolute_uri(profile.resume.url) if profile.resume else None
            ),
            "uploaded_at": profile.resume_uploaded_at,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_resume(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    serializer = ResumeSerializer(instance=profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    profile.resume_uploaded_at = timezone.now()
    profile.save(update_fields=["resume_uploaded_at"])
    return Response({"message": "Upload successful"}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_resume(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.resume:
        profile.resume.delete(save=False)
        profile.resume = None
        profile.resume_uploaded_at = None
        profile.save(update_fields=["resume", "resume_uploaded_at"])
    return Response(status=status.HTTP_204_NO_CONTENT)
