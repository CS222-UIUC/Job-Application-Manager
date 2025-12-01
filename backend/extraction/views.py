import ipaddress
import socket
from urllib.parse import urlparse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .extractor import analyze_jd, extract_jd_text
from .serializers import (
    ExtractRequestSerializer,
    ExtractResponseSerializer,
)

MAX_JD_CHARS = 10_000


def _is_private_host(url: str) -> bool:
    host = urlparse(url).hostname or ""
    try:
        ip = socket.gethostbyname(host)
        return ipaddress.ip_address(ip).is_private
    except Exception:
        return True


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def extract_jd(request):
    s = ExtractRequestSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    url = s.validated_data["url"]

    if _is_private_host(url):
        return Response({"detail": "Invalid or private host"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        text = extract_jd_text(url)
        MAX_LEN = 80_000
        text = text[:MAX_LEN]
        out = {"url": url, "text": text, "chars": len(text)}
        return Response(ExtractResponseSerializer(out).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": f"extract failed: {e}"}, status=status.HTTP_502_BAD_GATEWAY)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def extract_skills(request):
    req = ExtractRequestSerializer(data=request.data)
    req.is_valid(raise_exception=True)
    url = req.validated_data["url"]

    if _is_private_host(url):
        return Response({"detail": "Invalid or private host"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        jd_text = extract_jd_text(url)[:MAX_JD_CHARS]
    except Exception as e:
        return Response({"detail": f"Failed to fetch JD: {e}"}, status=status.HTTP_502_BAD_GATEWAY)

    try:
        analysis = analyze_jd(jd_text)
    except Exception as e:
        return Response(
            {"detail": f"Skill analysis failed: {e}"}, status=status.HTTP_502_BAD_GATEWAY
        )

    out = {
        "url": url,
        "job_title": analysis.get("job_title", "Not specified"),
        "company": analysis.get("company", "Not specified"),
        "location": analysis.get("location", "Not specified"),
        "responsibilities": analysis.get("responsibilities", []),
        "requirements": analysis.get("requirements", []),
        "categories": analysis.get("categories", []),
        "flat": analysis.get("flat", []),
        "leetcode_recommendations": analysis.get("leetcode_recommendations", []),
        "jd_chars": len(jd_text),
    }
    return Response(out, status=status.HTTP_200_OK)
