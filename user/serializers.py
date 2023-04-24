from rest_framework import serializers
from .models import CustomUser as CustomUserModel

class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = "__all__"