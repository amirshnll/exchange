from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Balance as BalanceModel
from .serializers import BalanceSerializers, BalanceValidationSerializer
from user.permissions import method_permission_classes, IsLogginedUser, IsAdmin


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
        order_serializer = BalanceValidationSerializer(data=request.data)

        if order_serializer.is_valid():
            user = order_serializer.validated_data["user"]
            balance = order_serializer.validated_data["balance"]
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            balance_obj = BalanceModel.objects.get(user=user)
        except BalanceModel.DoesNotExist:
            balance_serializer = BalanceSerializers(data={"user": user})
            if balance_serializer.is_valid():
                balance_serializer.save()
            else:
                return Response(
                    {"status": "error", "message": "balance does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        balance_obj = BalanceModel.objects.get(user=user)
        balance_obj.balance = balance
        balance_obj.save()
        serializer = BalanceSerializers(instance=balance_obj, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
