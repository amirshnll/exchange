from .models import CustomUser as CustomUserModel


def delete_user(user):
    try:
        user_obj = CustomUserModel.objects.get(pk=user)
        user_obj.delete()
        return True  # user deleted
    except CustomUserModel.DoesNotExist:
        return False  # user undeleted
