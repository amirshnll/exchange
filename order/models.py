from django.db import models
from user.models import CustomUser as CustomUserModel
from coin.models import CoinTypes as CoinTypesModel


class OrderStatus(models.TextChoices):
    PENDING = "PENDING"
    DONE = "DONE"


class Order(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    coin = models.ForeignKey(CoinTypesModel, on_delete=models.CASCADE)
    coin_amount = models.IntegerField()
    order_price = models.IntegerField()
    status = models.CharField(choices=OrderStatus.choices, max_length=10)
