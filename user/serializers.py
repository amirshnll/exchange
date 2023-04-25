from rest_framework import serializers
from .models import CustomUser as CustomUserModel, UserTypes as UserTypesModel


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
        user.type = UserTypesModel.CUSTOMER
        user.username = validated_data["username"]
        user.set_password(validated_data["password"])
        user.save()

        return user


class RegisterNewUserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUserModel()
        user.type = UserTypesModel.ADMIN
        user.username = validated_data["username"]
        user.set_password(validated_data["password"])
        user.save()

        return user


class AuthValidationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attribute):
        return attribute
