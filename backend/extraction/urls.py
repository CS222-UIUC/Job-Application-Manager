from django.urls import path

from . import views

urlpatterns = [
    path("extract_jd/", views.extract_jd, name="extract-jd"),
]
