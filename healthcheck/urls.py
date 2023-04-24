from django.urls import path
from .views import (
    HealthCheckApi,
)

urlpatterns = [
    path("", HealthCheckApi.as_view()),
]
