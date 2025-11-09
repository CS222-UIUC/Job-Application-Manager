import ipaddress
import socket
from urllib.parse import urlparse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .extractor import extract_jd_text
from .serializers import ExtractRequestSerializer, ExtractResponseSerializer


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
