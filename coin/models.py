from django.db import models


class CoinTypes(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
