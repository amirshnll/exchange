from django.urls import path
from .views import orderApi

urlpatterns = [
    path("", OrderApi.as_view()),
    path("<int:order_id>/", OrderApi.as_view()),
]
