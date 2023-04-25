from django.test import TestCase
from rest_framework.test import APIClient
from user.defs import get_token_prefix
import random

customer_user = {"username": "amir", "password": "ij4ZqGNwx9slG0Ltq4FS"}
admin_user = {"username": "admin", "password": "d6YHGGXncRFCTTXL4XYp"}


class OrderTestCases(TestCase):
    # python manage.py test order.tests.OrderTestCases.UserOrder
    def UserOrder(self):
        self.clients = APIClient()

        self.admin_register = self.client.post(
            "/api/v1/user/admin/",
            admin_user,
        ).json()

        auth_admin_obj = self.clients.post("/api/v1/user/auth/", admin_user).json()
        admin_token = get_token_prefix() + auth_admin_obj["token"]
        # print(admin_user["username"], admin_token)

        self.user_register = self.client.post(
            "/api/v1/user/",
            customer_user,
        ).json()

        auth_obj = self.clients.post("/api/v1/user/auth/", customer_user).json()
        user_token = get_token_prefix() + auth_obj["token"]

        user_balance = self.clients.get(
            "/api/v1/balance/user/", {}, **{"HTTP_AUTHORIZATION": user_token}
        ).json()

        self.clients.post(
            "/api/v1/balance/user/increase/",
            {"user": auth_obj["user_id"], "balance": random.randint(10, 100)},
            **{"HTTP_AUTHORIZATION": admin_token}
        ).json()

        user_balance = self.clients.get(
            "/api/v1/balance/user/", {}, **{"HTTP_AUTHORIZATION": user_token}
        ).json()
        print("balance before purchase: ", customer_user["username"], user_balance["balance"])

        new_coin = {"name": "ABAN", "symbol": "ABAN", "price": "4"}
        self.clients.post(
            "/api/v1/coin/", new_coin, **{"HTTP_AUTHORIZATION": admin_token}
        ).json()

        new_order = self.clients.post(
            "/api/v1/order/new/",
            {"name": "ABAN", "count": 3},
            **{"HTTP_AUTHORIZATION": user_token}
        ).json()
        print(new_order)

        user_balance = self.clients.get(
            "/api/v1/balance/user/", {}, **{"HTTP_AUTHORIZATION": user_token}
        ).json()
        print("balance after purchase: ", customer_user["username"], user_balance["balance"])
