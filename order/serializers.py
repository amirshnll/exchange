from rest_framework import serializers
from .models import Order as OrderModel


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderValidationSerializer(serializers.Serializer):
    coin = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)

    def validate(self, attribute):
        if attribute["amount"] <= 0:
            raise serializers.ValidationError(
                {"amount": "Must be positive and greater than zero."}
            )
        return attribute
