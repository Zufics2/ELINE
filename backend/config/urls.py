from django.urls import include, path

urlpatterns = [
    path("api/", include("apps.methods.urls")),
    path("api/", include("apps.solutions.urls")),
]
