from django.urls import path
from .views import UserApi, UserAdminApi, UserTypeList

urlpatterns = [
    path("", UserApi.as_view()),
    path("admin/", UserAdminApi.as_view()),
    path("type/list/", UserTypeList.as_view()),
]
