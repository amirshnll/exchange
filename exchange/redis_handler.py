import redis
from django.conf import settings


class RedisHandler:
    def __init__(self):
        self.redis_connection = redis.Redis(
            host=settings.REDIS_HOST, db=settings.REDIS_DB
        )

    def get_item(self, key_name):
        if self.redis_connection.exists(key_name):
            return int(self.redis_connection.get(key_name))
        else:
            return 0

    def set_item(self, key_name, value):
        if self.redis_connection.exists(key_name):
            self.remove_item(key_name)
            self.redis_connection.set(key_name, value)
        else:
            self.redis_connection.set(key_name, str(value))

    def remove_item(self, key_name):
        self.redis_connection.delete(key_name)
