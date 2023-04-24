from rest_framework import serializers
from .models import Order as OrderModel
from coin.defs import coin_is_exists


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderValidationSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    count = serializers.IntegerField(required=True)

    def validate(self, attribute):
        if attribute["count"] <= 0:
            raise serializers.ValidationError({"count": "count must greater than zero"})
        elif coin_is_exists(attribute["name"]) is False:
            raise serializers.ValidationError({"name": "this coin not exists"})
        return attribute
