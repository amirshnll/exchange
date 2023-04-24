from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Balance as BalanceModel
from .serializers import BalanceSerializers


class BalanceApi(APIView):
    # create balance
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
    def get(self, request, balance_id):
        try:
            balance_obj = BalanceModel.objects.get(pk=balance_id)
        except BalanceModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "DoesNotExist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_serializer = BalanceSerializers(instance=balance_obj, many=False)
        return Response(balance_serializer.data, status=status.HTTP_200_OK)

    # update balance by balance_id
    def put(self, request, balance_id):
        try:
            balance_obj = BalanceModel.objects.get(pk=balance_id)
        except BalanceModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "DoesNotExist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_obj.balance = (
            request.data["balance"] if "balance" in request.data else 0
        )
        balance_obj.save()
        serializer = BalanceSerializers(instance=balance_obj, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete balance by balance_id
    def delete(self, request, balance_id):
        try:
            balance_obj = BalanceModel.objects.get(pk=int(balance_id))
        except BalanceModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "DoesNotExist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_obj.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class UserBalanceApi(APIView):
    # get user balance by user
    def get(self, request):
        try:
            balance_obj = BalanceModel.objects.get(user=request.user.id)
        except BalanceModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "DoesNotExist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_serializer = BalanceSerializers(instance=balance_obj, many=False)
        return Response(balance_serializer.data, status=status.HTTP_200_OK)

    # update balance by user
    def put(self, request):
        try:
            balance_obj = BalanceModel.objects.get(user=request.user.id)
        except BalanceModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "DoesNotExist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        balance_obj.balance = (
            request.data["balance"] if "balance" in request.data else 0
        )
        balance_obj.save()
        serializer = BalanceSerializers(instance=balance_obj, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
