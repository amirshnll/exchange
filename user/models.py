from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_deleted = models.BooleanField(default=False)
