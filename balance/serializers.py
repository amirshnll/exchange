from rest_framework import serializers
from .models import Balance as BalanceModel


class BalanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = BalanceModel
        fields = "__all__"
