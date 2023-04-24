from django.urls import path
from .views import UserApi, UserAdminApi

urlpatterns = [
    path("", UserApi.as_view()),
    path("admin/", UserAdminApi.as_view()),
]
