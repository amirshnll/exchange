from django.db import models
from user.models import CustomUser as CustomUserModel


class Balance(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
