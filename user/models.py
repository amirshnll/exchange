from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from balance.serializers import BalanceSerializers
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    is_deleted = models.BooleanField(default=False)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user(sender, instance, created=False, **kwargs):
        if created:
            # create user balance
            serializer = BalanceSerializers(data={"user": instance})
            if serializer.is_valid():
                serializer.save()
            else:
                # roll back user registered
                try:
                    user_obj = CustomUser.objects.get(pk=instance)
                    user_obj.delete()
                except CustomUser.DoesNotExist:
                    pass
