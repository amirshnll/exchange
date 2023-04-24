from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    is_deleted = models.BooleanField(default=False)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user(sender, instance, created=False, **kwargs):
        if created:
            # create user balance
            from balance.defs import create_new_user_balance # circular import
            user_balance_status = create_new_user_balance(instance)
            if user_balance_status == False:
                # roll back user registered
                try:
                    user_obj = CustomUser.objects.get(pk=instance)
                    user_obj.delete()
                except CustomUser.DoesNotExist:
                    pass
