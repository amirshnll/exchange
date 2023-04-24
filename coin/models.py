from django.db import models


class CoinTypes(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    price = models.FloatField(
        default=0,
    )
    minimum_purchase = models.IntegerField(default=0, null=True, blank=True)
