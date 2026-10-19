from django.urls import path

from . import views

urlpatterns = [
    path("solutions/", views.SolutionListCreateView.as_view()),
    path("solutions/<int:pk>/", views.SolutionDetailView.as_view()),
    path("tasks/<str:task_id>/", views.TaskStatusView.as_view()),
]
