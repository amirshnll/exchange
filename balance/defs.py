from .serializers import BalanceSerializers


def create_new_user_balance(user):
    serializer = BalanceSerializers(data={"user": user})
    if serializer.is_valid():
        serializer.save()
        return True  # user balance created

    return False  # user balance uncreated
