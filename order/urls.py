from django.urls import path
from .views import OrderApi, OrderStatusList, NewOrderApi

urlpatterns = [
    path("", OrderApi.as_view()),
    path("<int:order_id>/", OrderApi.as_view()),
    path("status/list/", OrderStatusList.as_view()),
    path("new/", NewOrderApi.as_view()),
]
