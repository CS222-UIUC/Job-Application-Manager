from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import LeetCodeRecord
from .serializers import LeetCodeRecordSerializer

class LeetCodeRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LeetCodeRecordSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["difficulty","status"]
    search_fields = ["title","problem_id","tags"]
    ordering_fields = ["solved_at","updated_at","time_spent_min"]

    def get_queryset(self):
        return LeetCodeRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
