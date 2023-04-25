from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser as CustomUserModel, UserTypes as UserTypesModel
from .serializers import (
    CustomUserSerializers,
    RegisterNewUserSerializer,
    RegisterNewUserAdminSerializer,
)
from .permissions import method_permission_classes, IsLogginedUser
from rest_framework_simplejwt.tokens import RefreshToken


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
    # create new admin
    def post(self, request):
        serializer = RegisterNewUserAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if serializer.errors.get("username"):
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTypeList(APIView):
    # user type list
    def get(self, request):
        response = [i[0] for i in UserTypesModel.choices]
        return Response(response, status=status.HTTP_200_OK)


class UserAuthApi(APIView):
    # auth user
    def post(self, request):
        if "username" in request.data:
            username = request.data["username"]
        else:
            return Response(
                {"status": "username not received"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "password" in request.data:
            password = request.data["password"]
        else:
            return Response(
                {"status": "password not received"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_obj = CustomUserModel.objects.get(username=username, is_deleted=False)
        except CustomUserModel.DoesNotExist:
            return Response(
                {
                    "detail": "error",
                    "message": "invalid username or password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_obj.check_password(password):
            user_token = RefreshToken.for_user(user_obj)
            response = {
                "token": str(user_token.access_token),
                "refresh": str(user_token),
                "user_id": user_obj.id,
                "username": user_obj.username,
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "detail": "error",
                    "message": "invalid username/email or password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
