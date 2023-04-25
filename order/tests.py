from django.test import TestCase
from rest_framework.test import APIClient
from user.defs import get_token_prefix
import random

customer_user = {"username": "amir", "password": "ij4ZqGNwx9slG0Ltq4FS"}
admin_user = {"username": "admin", "password": "d6YHGGXncRFCTTXL4XYp"}

customers_list = [
    {"username": "amir", "password": "ij4ZqGNwx9slG0Ltq4FS"},
    {"username": "nilo", "password": "p8VeqZOwHlQa7X2IFeY3"},
    {"username": "hanie", "password": "yF5kScZLdQQhK4niOQw0"},
]


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
        print(
            "balance before purchase: ",
            customer_user["username"],
            user_balance["balance"],
        )

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
        print(
            "balance after purchase: ",
            customer_user["username"],
            user_balance["balance"],
        )

    # python manage.py test order.tests.OrderTestCases.MultipleUserOrder
    def MultipleUserOrder(self):
        self.clients = APIClient()

        self.admin_register = self.client.post(
            "/api/v1/user/admin/",
            admin_user,
        ).json()

        auth_admin_obj = self.clients.post("/api/v1/user/auth/", admin_user).json()
        admin_token = get_token_prefix() + auth_admin_obj["token"]
        # print(admin_user["username"], admin_token)

        new_coin = {"name": "ABAN", "symbol": "ABAN", "price": "4"}
        self.clients.post(
            "/api/v1/coin/", new_coin, **{"HTTP_AUTHORIZATION": admin_token}
        ).json()

        for user in customers_list:
            self.user_register = self.client.post(
                "/api/v1/user/",
                user,
            ).json()

            auth_obj = self.clients.post("/api/v1/user/auth/", user).json()
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
            """print(
                "balance before purchase: ",
                user["username"],
                user_balance["balance"],
            )"""

            new_order = self.clients.post(
                "/api/v1/order/new/",
                {"name": "ABAN", "count": 1},
                **{"HTTP_AUTHORIZATION": user_token}
            ).json()
            print(new_order)

            user_balance = self.clients.get(
                "/api/v1/balance/user/", {}, **{"HTTP_AUTHORIZATION": user_token}
            ).json()
            """print(
                "balance after purchase: ",
                user["username"],
                user_balance["balance"],
            )"""
