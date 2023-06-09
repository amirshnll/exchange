from exchange.redis_handler import RedisHandler
from coin.models import CoinTypes as CoinTypesModel
from .models import Order as OrderModel, OrderStatus as OrderStatusModel


class PandingOrderHandler:
    def _get_coin(self, coin_id):
        try:
            return CoinTypesModel.objects.get(pk=coin_id)
        except CoinTypesModel.DoesNotExist:
            return None

    def _set_pending_order_done(self, coin_id):
        OrderModel.objects.filter(coin=coin_id, status=OrderStatusModel.PENDING).update(
            status=OrderStatusModel.DONE
        )

    def pending_order(self, coin_id):
        coin_obj = self._get_coin(coin_id=coin_id)
        if coin_obj is None:
            return 0

        # get pending count
        pending_count = self.get_pending_count(coin_id=coin_obj.id)

        # change pending order status
        if pending_count > 0:
            self._set_pending_order_done(coin_id=coin_obj.id)

            # remove pending from redis
            redis_handler = RedisHandler()
            redis_handler.remove_item(coin_obj.id)

        return pending_count

    def get_pending_count(self, coin_id):
        redis_handler = RedisHandler()
        return redis_handler.get_item(coin_id)

    def set_pending(self, coin_id, value):
        redis_handler = RedisHandler()
        old_value = self.get_pending_count(coin_id=coin_id)
        redis_handler.set_item(coin_id, old_value + value)
