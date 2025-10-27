

urlpatterns = [
    path("", views.get_applications, name="applications-list"),
    path("create/", views.create_application, name="application-create"),
    # new api endpoints, match the frontend data format
    path("jobs/", views.get_job_applications, name="job-applications-list"),
    path("jobs/create/", views.create_job_application, name="job-application-create"),
]
