from django.urls import path
from .views import UserApi

urlpatterns = [
    path("", UserApi.as_view()),
]
