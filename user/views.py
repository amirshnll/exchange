from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser as CustomUserModel
from .serializers import (
    CustomUserSerializers,
    RegisterNewUserSerializer,
    RegisterNewUserAdminSerializer,
)
from .permissions import method_permission_classes, IsLogginedUser


class UserApi(APIView):
    # get user
    @method_permission_classes([IsLogginedUser])
    def get(self, request):
        try:
            user_obj = CustomUserModel.objects.get(pk=request.user.id)
        except CustomUserModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "user does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_serializer = CustomUserSerializers(instance=user_obj, many=False)
        return Response(balance_serializer.data, status=status.HTTP_200_OK)

    # create new user
    def post(self, request):
        serializer = RegisterNewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if serializer.errors.get("username"):
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAdminApi(APIView):
    # create new user
    def post(self, request):
        serializer = RegisterNewUserAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if serializer.errors.get("username"):
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
