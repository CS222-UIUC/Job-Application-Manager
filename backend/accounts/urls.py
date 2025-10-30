from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.user_profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("check-auth/", views.check_auth, name="check_auth"),
    path("get-resume/", views.get_resume, name="get_resume"),
    path("upload-resume/", views.post_resume, name="upload_resume"),
    path("delete-resume/", views.delete_resume, name="delete_resume"),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # for development
