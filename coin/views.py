from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CoinTypes as CoinTypesModel
from .serializers import CoinTypesSerializers
from user.permissions import method_permission_classes, IsLogginedUser, IsAdmin


class CoinApi(APIView):
    # create coin
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def post(self, request):
        coin_serializer = CoinTypesSerializers(data=request.data)
        if not coin_serializer.is_valid():
            return Response(coin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        coin_serializer.save()
        return Response(coin_serializer.data, status=status.HTTP_201_CREATED)

    # get coin data
    @method_permission_classes([IsLogginedUser])
    def get(self, request, coin_id):
        try:
            coin_obj = CoinTypesModel.objects.get(pk=coin_id)
        except CoinTypesModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "coin does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        coin_serializer = CoinTypesSerializers(instance=coin_obj, many=False)
        return Response(coin_serializer.data, status=status.HTTP_200_OK)

    # update coin by coin_id
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def put(self, request, coin_id):
        try:
            coin_obj = CoinTypesModel.objects.get(pk=coin_id)
        except CoinTypesModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "coin does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "name" in request.data:
            coin_obj.name = request.data["balance"]
        if "symbol" in request.data:
            coin_obj.symbol = request.data["symbol"]
        if "price" in request.data and request.data["price"] > 0:
            coin_obj.price = request.data["price"]
        coin_obj.save()
        serializer = CoinTypesSerializers(instance=coin_obj, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete coin by coin_id
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def delete(self, request, coin_id):
        try:
            coin_obj = CoinTypesModel.objects.get(pk=coin_id)
        except CoinTypesModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "coin does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        coin_obj.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
