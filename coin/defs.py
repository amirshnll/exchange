from .models import CoinTypes as CoinTypesModel


def coin_is_exists(coin_name):
    try:
        coin_obj = CoinTypesModel.objects.get(name=coin_name)
        return True
    except CoinTypesModel.DoesNotExist:
        return False
