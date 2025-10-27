from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_applications, name="applications-list"),
    path("create/", views.create_application, name="application-create"),
]
