from rest_framework import permissions


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)

        return decorated_func

    return decorator


class IsLogginedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.id is not None
            and request.user.id > 0
            and request.user.is_deleted == False
        ):
            return True
        else:
            return False
