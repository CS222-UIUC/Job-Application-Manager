import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import LeetCodeRecord
from .serializers import LeetCodeRecordSerializer


class LeetCodeRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LeetCodeRecordSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["difficulty", "status"]
    search_fields = ["title", "problem_id", "tags"]
    ordering_fields = ["solved_at", "updated_at", "time_spent_min"]

    def get_queryset(self):
        return LeetCodeRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_leetcode_problem(request, problem_number):
    try:
        # LeetCode GraphQL API
        query = """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
          problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
          ) {
            questions: data {
              questionId
              title
              titleSlug
              difficulty
              topicTags {
                name
              }
            }
          }
        }
        """

        variables = {"categorySlug": "", "skip": problem_number - 1, "limit": 1, "filters": {}}

        response = requests.post(
            "https://leetcode.com/graphql",
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
        )

        data = response.json()

        if data.get("data") and data["data"]["problemsetQuestionList"]["questions"]:
            problem = data["data"]["problemsetQuestionList"]["questions"][0]

            # Verify if the problem number matches
            if int(problem["questionId"]) != problem_number:
                return Response(
                    {"error": f"Problem #{problem_number} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {
                    "number": int(problem["questionId"]),
                    "name": problem["title"],
                    "slug": problem["titleSlug"],
                    "difficulty": problem["difficulty"],
                    "topics": [tag["name"] for tag in problem["topicTags"]],
                    "url": f"https://leetcode.com/problems/{problem['titleSlug']}/",
                }
            )
        else:
            return Response(
                {"error": f"Problem #{problem_number} not found"}, status=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
