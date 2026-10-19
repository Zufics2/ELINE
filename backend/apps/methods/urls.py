from django.urls import path

from .views import MethodListView

urlpatterns = [path("methods/", MethodListView.as_view())]
