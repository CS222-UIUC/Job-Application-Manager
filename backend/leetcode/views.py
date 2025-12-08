from rest_framework import permissions, viewsets

from .models import LeetCodeProblem, UserProblemRecord
from .serializers import LeetCodeProblemSerializer, UserProblemRecordSerializer


class LeetCodeProblemViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = LeetCodeProblem.objects.all().order_by("problem_id")
    serializer_class = LeetCodeProblemSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProblemRecordViewSet(viewsets.ModelViewSet):

    serializer_class = UserProblemRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return user records
        return UserProblemRecord.objects.filter(user=self.request.user).select_related("problem")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
