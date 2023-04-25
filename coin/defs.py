from .models import CoinTypes as CoinTypesModel


def coin_is_exists(coin_name):
    return CoinTypesModel.objects.filter(name=coin_name).exists()
