from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Balance as BalanceModel
from .serializers import BalanceSerializers, BalanceValidationSerializer
from user.permissions import method_permission_classes, IsLogginedUser, IsAdmin
from .balance_handler import BalanceHandler


class BalanceApi(APIView):
    # create balance
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def post(self, request):
        balance_serializer = BalanceSerializers(data=request.data)
        if balance_serializer.is_valid():
            balance_serializer.save()
            return Response(balance_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                balance_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    # get user balance
    @method_permission_classes([IsLogginedUser])
    def get(self, request, balance_id):
        try:
            balance_obj = BalanceModel.objects.get(pk=balance_id)
        except BalanceModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "balance does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_serializer = BalanceSerializers(instance=balance_obj, many=False)
        return Response(balance_serializer.data, status=status.HTTP_200_OK)

    # update balance by balance_id
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def put(self, request, balance_id):
        try:
            balance_obj = BalanceModel.objects.get(pk=balance_id)
        except BalanceModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "balance does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_obj.balance = (
            request.data["balance"] if "balance" in request.data else 0
        )
        balance_obj.save()
        serializer = BalanceSerializers(instance=balance_obj, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete balance by balance_id
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def delete(self, request, balance_id):
        try:
            balance_obj = BalanceModel.objects.get(pk=balance_id)
        except BalanceModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "balance does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_obj.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class UserBalanceApi(APIView):
    # get user balance by user
    @method_permission_classes([IsLogginedUser])
    def get(self, request):
        try:
            balance_obj = BalanceModel.objects.get(user=request.user.id)
        except BalanceModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "balance does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_serializer = BalanceSerializers(instance=balance_obj, many=False)
        return Response(balance_serializer.data, status=status.HTTP_200_OK)

    # update balance by user
    @method_permission_classes([IsLogginedUser])
    def put(self, request):
        try:
            balance_obj = BalanceModel.objects.get(user=request.user.id)
        except BalanceModel.DoesNotExist:
            balance_serializer = BalanceSerializers(data={"user": request.user.id})
            if balance_serializer.is_valid():
                balance_serializer.save()
            else:
                return Response(
                    {"status": "error", "message": "balance does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        balance_obj = BalanceModel.objects.get(user=request.user.id)
        balance_obj.balance = (
            request.data["balance"] if "balance" in request.data else 0
        )
        balance_obj.save()
        serializer = BalanceSerializers(instance=balance_obj, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeUserBalanceApi(APIView):
    # update balance user
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def post(self, request):
        balance_serializer = BalanceValidationSerializer(data=request.data)

        if balance_serializer.is_valid():
            user = balance_serializer.validated_data["user"]
            balance = balance_serializer.validated_data["balance"]
        else:
            return Response(
                balance_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        balance_handler = BalanceHandler()
        balance_handler.set(user_id=user, new_value=balance)
        balance_obj = balance_handler.get(user_id=user)
        balance_serializer = BalanceSerializers(instance=balance_obj, many=False)

        return Response(balance_serializer.data, status=status.HTTP_200_OK)


class IncreaseUserBalanceApi(APIView):
    # increase balance user
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def post(self, request):
        balance_serializer = BalanceValidationSerializer(data=request.data)

        if balance_serializer.is_valid():
            user = balance_serializer.validated_data["user"]
            balance = balance_serializer.validated_data["balance"]
        else:
            return Response(
                balance_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        balance_handler = BalanceHandler()
        balance_handler.increase(user_id=user, increased_value=balance)
        balance_obj = balance_handler.get(user_id=user)

        result = None
        if balance_obj is not None:
            balance_serializer = BalanceSerializers(instance=balance_obj, many=False)
            result = balance_serializer.data

        return Response(result, status=status.HTTP_200_OK)


class DecreaseUserBalanceApi(APIView):
    # decrease balance user
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def post(self, request):
        balance_serializer = BalanceValidationSerializer(data=request.data)

        if balance_serializer.is_valid():
            user = balance_serializer.validated_data["user"]
            balance = balance_serializer.validated_data["balance"]
        else:
            return Response(
                balance_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        balance_handler = BalanceHandler()
        balance_handler.decrease(user_id=user, decreased_value=balance)
        balance_obj = balance_handler.get(user_id=user)

        result = None
        if balance_obj is not None:
            balance_serializer = BalanceSerializers(instance=balance_obj, many=False)
            result = balance_serializer.data

        return Response(result, status=status.HTTP_200_OK)
