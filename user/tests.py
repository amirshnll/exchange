from django.test import TestCase
from rest_framework.test import APIClient
from .defs import get_token_prefix

user_list = [
    {"username": "amir", "password": "ij4ZqGNwx9slG0Ltq4FS"},
    {"username": "nilo", "password": "p8VeqZOwHlQa7X2IFeY3"},
    {"username": "hanie", "password": "yF5kScZLdQQhK4niOQw0"},
]


class UserTestCases(TestCase):
    # python manage.py test user.tests.UserTestCases.UserAuth
    def test_UserAuth(self):
        self.clients = APIClient()
        for user in user_list:
            self.user_register = self.client.post(
                "/api/v1/user/",
                user,
            ).json()

            auth_obj = self.clients.post("/api/v1/user/auth/", user).json()
            user_token = get_token_prefix() + auth_obj["token"]
            print(user["username"], user_token)
