from exchange.redis_handler import RedisHandler
from coin.models import CoinTypes as CoinTypesModel
from .models import Order as OrderModel, OrderStatus as OrderStatusModel


class PandingOrderHandler:
    def _get_coin(self, coin_id):
        try:
            coin_obj = CoinTypesModel.objects.get(id=coin_id)
            return coin_obj
        except CoinTypesModel.DoesNotExist:
            return None

    def _add_pending(self, coin_id, value):
        redis_handler = RedisHandler()
        redis_handler.set_item(coin_id, value)

    def _update_pending(self, coin_id, value):
        redis_handler = RedisHandler()
        old_value = self.get_pending_count(coin_id=coin_id)
        redis_handler.remove_item(coin_id, value)
        redis_handler.set_item(coin_id, old_value + value)

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
        pending_count = redis_handler.get_item(coin_id)
        if pending_count:
            return int.from_bytes(
                pending_count,
                byteorder="little",
            )

        return 0

    def set_pending(self, coin_id, value):
        if self.get_pending_count(coin_id=coin_id) > 0:
            self._update_pending(coin_id=coin_id, value=value)
        else:
            self._add_pending(coin_id=coin_id, value=value)
