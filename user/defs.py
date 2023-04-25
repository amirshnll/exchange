from .models import CustomUser as CustomUserModel
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def delete_user(user):
    try:
        user_obj = CustomUserModel.objects.get(pk=user)
        user_obj.delete()
        return True  # user deleted
    except CustomUserModel.DoesNotExist:
        return False  # user undeleted


def get_token_prefix():
    return str(settings.AUTH_PREFIX) + " "


def user_is_exists(user_id):
    try:
        user_obj = CustomUserModel.objects.get(pk=user_id)
        return True
    except CustomUserModel.DoesNotExist:
        return False


def make_auth_obj(user_obj):
    user_token = RefreshToken.for_user(user_obj)
    return {
        "token": str(user_token.access_token),
        "refresh": str(user_token),
        "user_id": user_obj.id,
        "username": user_obj.username,
    }
