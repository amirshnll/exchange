from django.urls import path
from .views import CoinApi

urlpatterns = [
    path("", CoinApi.as_view()),
    path("<int:coin_id>/", CoinApi.as_view()),
]
