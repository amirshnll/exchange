from rest_framework import serializers
from .models import CustomUser as CustomUserModel


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = "__all__"


class RegisterNewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUserModel()
        user.type = validated_data["type"]
        user.username = validated_data["username"]
        user.set_password(validated_data["password"])
        user.save()

        return user
