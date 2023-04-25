from django.test import TestCase
from rest_framework.test import APIClient
from .defs import get_token_prefix

user_list = [
    {"username": "amir", "password": "ij4ZqGNwx9slG0Ltq4FS"},
    {"username": "nilo", "password": "p8VeqZOwHlQa7X2IFeY3"},
    {"username": "hanie", "password": "yF5kScZLdQQhK4niOQw0"},
]


class OrderTestCases(TestCase):
    # python manage.py test user.tests.OrderTestCases.User
    def UserAuth(self):
        for user in user_list:
            self.clients = APIClient()
            self.user_register = self.client.post(
                "/api/v1/user/",
                user,
            ).json()

            auth_obj = self.clients.post('/api/v1/user/auth/', user).json()
            user_token = get_token_prefix() + auth_obj["token"]
            self.clients.credentials(HTTP_AUTHORIZATION=user_token)

