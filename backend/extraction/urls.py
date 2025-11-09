from django.urls import path

from . import views

urlpatterns = [
    path("extract_jd/", views.extract_jd, name="extract-jd"),
    path("extract_skills/", views.extract_skills, name="extract-skills"),
]
