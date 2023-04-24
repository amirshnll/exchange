from rest_framework import serializers
from .models import Order as OrderModel


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"
