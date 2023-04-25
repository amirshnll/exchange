from django.urls import path
from .views import UserApi, UserAdminApi, UserTypeList, UserAuthApi

urlpatterns = [
    path("", UserApi.as_view()),
    path("admin/", UserAdminApi.as_view()),
    path("type/list/", UserTypeList.as_view()),
    path("auth/", UserAuthApi.as_view()),
]
