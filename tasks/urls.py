from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import TaskViewSet

routers = DefaultRouter()

routers.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(routers.urls)),
]
