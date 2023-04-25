from rest_framework import serializers
from .models import Balance as BalanceModel
from user.defs import user_is_exists


class BalanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = BalanceModel
        fields = "__all__"


class BalanceValidationSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True)
    balance = serializers.IntegerField(required=True)

    def validate(self, attribute):
        if attribute["balance"] <= 0:
            raise serializers.ValidationError(
                {"balance": "balance must greater than zero"}
            )
        elif user_is_exists(attribute["user"]) is False:
            raise serializers.ValidationError({"user": "this user not exists"})
        return attribute
