from django.urls import path
from .views import OrderApi

urlpatterns = [
    path("", OrderApi.as_view()),
    path("<int:order_id>/", OrderApi.as_view()),
]
