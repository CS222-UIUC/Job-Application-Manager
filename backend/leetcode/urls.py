from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LeetCodeProblemViewSet, UserProblemRecordViewSet

router = DefaultRouter()
router.register("problems", LeetCodeProblemViewSet, basename="leetcode-problem")
router.register("records", UserProblemRecordViewSet, basename="leetcode-record")

urlpatterns = [
    path("", include(router.urls)),
]
