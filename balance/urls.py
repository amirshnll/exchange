from django.urls import path
from .views import (
    BalanceApi,
    UserBalanceApi,
    ChangeUserBalanceApi,
    IncreaseUserBalanceApi,
    DecreaseUserBalanceApi,
)

urlpatterns = [
    path("", BalanceApi.as_view()),
    path("<int:balance_id>/", BalanceApi.as_view()),
    path("user/", UserBalanceApi.as_view()),
    path("user/change_balance/", ChangeUserBalanceApi.as_view()),
    path("user/increase/", IncreaseUserBalanceApi.as_view()),
    path("user/decrease/", DecreaseUserBalanceApi.as_view()),
]
