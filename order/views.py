from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order as OrderModel, OrderStatus as OrderStatusModel
from .serializers import OrderSerializers, OrderValidationSerializer
from user.permissions import method_permission_classes, IsLogginedUser, IsAdmin
from balance.balance_handler import BalanceHandler
from django.conf import settings
from coin.models import CoinTypes as CoinTypesModel
from exchange.exchange_handler import ExternalExchangeHandler
from .pending_order_handler import PandingOrderHandler


class OrderApi(APIView):
    # create order
    @method_permission_classes([IsLogginedUser])
    def post(self, request):
        order_serializer = OrderValidationSerializer(data=request.data)
        if not order_serializer.is_valid():
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        order_serializer = OrderSerializers(data=request.data)
        if not order_serializer.is_valid():
            return Response(
                order_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        order_serializer.save()
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

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
        order_obj.coin_count = (
            request.data["coin_count"] if "coin_count" in request.data else 0
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
        order_serializer = OrderValidationSerializer(data=request.data)

        if not order_serializer.is_valid():
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        name = order_serializer.validated_data["name"]
        count = order_serializer.validated_data["count"]

        coin_obj = CoinTypesModel.objects.get(name=name)

        purchase_price = count * int(coin_obj.price)

        balance_handler = BalanceHandler()
        if (
            balance_handler.is_enough(user_id=request.user.id, value=purchase_price)
            == False
        ):
            return Response(
                {"status": "error", "message": "user balance is not enough"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # new order obj
        new_order = {
            "user": request.user.id,
            "coin": coin_obj.id,
            "coin_count": count,
            "order_price": purchase_price,
            "status": OrderStatusModel.PENDING,
        }

        # set purchase status condition minimum per purchase
        if purchase_price >= settings.MINIMUM_PER_PURCHASE:
            new_order["status"] = OrderStatusModel.DONE

        # pending order handler
        pending_order_handler = PandingOrderHandler()

        order_serializer = OrderSerializers(data=new_order)
        if order_serializer.is_valid():
            order_serializer.save()

            balance_handler.decrease(
                user_id=request.user.id, decreased_value=purchase_price
            )

            if order_serializer.data["status"] == OrderStatusModel.DONE:
                pending_count = pending_order_handler.pending_order(
                    coin_id=coin_obj.id
                )
                exchange_count = purchase_price + pending_count

                # call exchange
                external_exchange_handler = ExternalExchangeHandler()
                external_exchange_handler.buy_from_exchange(
                    coin_name=coin_obj.name, count=exchange_count
                )
            else:
                pending_count = pending_order_handler.get_pending_count(
                    coin_id=coin_obj.id
                )
                if pending_count + purchase_price >= settings.MINIMUM_PER_PURCHASE:
                    pending_count = pending_order_handler.pending_order(
                        coin_id=coin_obj.id
                    )
                    exchange_count = purchase_price + pending_count

                    # call exchange
                    external_exchange_handler = ExternalExchangeHandler()
                    external_exchange_handler.buy_from_exchange(
                        coin_name=coin_obj.name, count=exchange_count
                    )
                else:
                    pending_order_handler.set_pending(
                        coin_id=coin_obj.id, value=purchase_price
                    )

        return Response({"status": "success"}, status=status.HTTP_200_OK)
