from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_applications, name="get_applications"),
    path("create/", views.create_application, name="create_application"),
    path("delete/<int:pk>/", views.delete_application, name="delete_application"),
]
