<<<<<<< HEAD
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet

router = DefaultRouter()
router.register(r"applications", ApplicationViewSet, basename="application")
urlpatterns = router.urls
=======
from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_applications, name="applications-list"),
    path("create/", views.create_application, name="application-create"),
]
>>>>>>> 50ba53588e1a87fb00805b17f1345ec046ecbd13
