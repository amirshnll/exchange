from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order as OrderModel, OrderStatus as OrderStatusModel
from .serializers import OrderSerializers
from user.permissions import method_permission_classes, IsLogginedUser, IsAdmin
from coin.defs import coin_is_exists


class OrderApi(APIView):
    # create order
    @method_permission_classes([IsLogginedUser])
    def post(self, request):
        order_serializer = OrderSerializers(data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # get order
    @method_permission_classes([IsLogginedUser])
    def get(self, request, order_id):
        try:
            order_obj = OrderModel.objects.get(pk=order_id)
        except OrderModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "order does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_serializer = OrderSerializers(instance=order_obj, many=False)
        return Response(order_serializer.data, status=status.HTTP_200_OK)

    # update order by order_id
    @method_permission_classes([IsLogginedUser])
    def put(self, request, order_id):
        try:
            order_obj = OrderModel.objects.get(pk=order_id)
        except OrderModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "order does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_obj.coin = request.data["coin"] if "coin" in request.data else 0
        order_obj.coin_amount = (
            request.data["coin_amount"] if "coin_amount" in request.data else 0
        )
        order_obj.order_price = (
            request.data["order_price"] if "order_price" in request.data else 0
        )
        order_obj.status = (
            request.data["status"]
            if "status" in request.data and request.data["status"] in OrderStatusModel
            else 0
        )
        order_obj.save()
        serializer = OrderSerializers(instance=order_obj, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete order by order_id
    @method_permission_classes([IsLogginedUser, IsAdmin])
    def delete(self, request, order_id):
        try:
            order_obj = OrderModel.objects.get(pk=order_id)
        except OrderModel.DoesNotExist:
            return Response(
                {"status": "error", "message": "order does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_obj.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class OrderStatusList(APIView):
    # order status list
    def get(self, request):
        response = [i[0] for i in OrderStatusModel.choices]
        return Response(response, status=status.HTTP_200_OK)


class NewOrderApi(APIView):
    # new order
    @method_permission_classes([IsLogginedUser])
    def post(self, request):
        if "name" in request.data:
            name = request.data["name"]
        else:
            return Response(
                {"status": "coin name not received"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "count" in request.data:
            count = int(request.data["count"])
            if count <= 0:
                return Response(
                    {"status": "count must greater than zero"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"status": "count not received"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if coin_is_exists(name) is False:
            return Response(
                {"status": "this coin not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "ok"}, status=status.HTTP_200_OK)
