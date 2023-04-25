from django.test import TestCase
from rest_framework.test import APIClient
from user.defs import get_token_prefix
import random

user_list = [
    {"username": "amir", "password": "ij4ZqGNwx9slG0Ltq4FS"},
    {"username": "nilo", "password": "p8VeqZOwHlQa7X2IFeY3"},
    {"username": "hanie", "password": "yF5kScZLdQQhK4niOQw0"},
]

admin_user = {"username": "admin", "password": "d6YHGGXncRFCTTXL4XYp"}


class BalanceTestCases(TestCase):
    # python manage.py test balance.tests.BalanceTestCases.UserBalance
    def test_UserBalance(self):
        self.clients = APIClient()

        self.admin_register = self.client.post(
            "/api/v1/user/admin/",
            admin_user,
        ).json()

        auth_admin_obj = self.clients.post("/api/v1/user/auth/", admin_user).json()
        admin_token = get_token_prefix() + auth_admin_obj["token"]
        # print(admin_user["username"], admin_token)

        for user in user_list:
            self.user_register = self.client.post(
                "/api/v1/user/",
                user,
            ).json()

            auth_obj = self.clients.post("/api/v1/user/auth/", user).json()
            user_token = get_token_prefix() + auth_obj["token"]

            user_balance = self.clients.get(
                "/api/v1/balance/user/", {}, **{"HTTP_AUTHORIZATION": user_token}
            ).json()
            # print("old balance: ", user["username"], user_balance["balance"])

            self.clients.post(
                "/api/v1/balance/user/increase/",
                {"user": auth_obj["user_id"], "balance": random.randint(10, 100)},
                **{"HTTP_AUTHORIZATION": admin_token}
            ).json()

            user_balance = self.clients.get(
                "/api/v1/balance/user/", {}, **{"HTTP_AUTHORIZATION": user_token}
            ).json()
            # print("new balance: ", user["username"], user_balance["balance"])
