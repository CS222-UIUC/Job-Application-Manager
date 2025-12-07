from django.urls import path

from . import views

urlpatterns = [
    path("problem/<int:problem_number>/", views.get_leetcode_problem, name="get_leetcode_problem"),
]
