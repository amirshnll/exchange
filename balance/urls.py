from django.urls import path
from .views import BalanceApi

urlpatterns = [
    path("", BalanceApi.as_view()),
    path("<int:balance_id>/", BalanceApi.as_view()),
]
