from rest_framework import serializers
from .models import CoinTypes as CoinTypesModel


class CoinTypesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoinTypesModel
        fields = "__all__"
