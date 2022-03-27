from os import sep
import environ
import base64
from rest_framework import status, HTTP_HEADER_ENCODING
from rest_framework.test import APITestCase
from django.test import Client

env = environ.Env()
environ.Env.read_env()

# Create your tests here.
class AuthenticationClass(APITestCase):
    def setUp(self):
        self.username = "azr1"
        self.password = "20S0KPNOIM"
        self.base_url = f"{env('APP_URL')}:{env('APP_PORT')}/"
        self.auth_header = {
            "HTTP_AUTHORIZATION": "Basic "
            + base64.b64encode(
                f"{self.username}:{self.password}".encode(HTTP_HEADER_ENCODING)
            ).decode(HTTP_HEADER_ENCODING)
        }
        self.client = Client()

    def test_valid_authentication(self):
        response = self.client.get(self.base_url, **self.auth_header)
        print("Response CODE: ", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_authentication(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_inbound_sms(self):
        payload = {"from": "", "to": "", "text": "Hello world!"}

    def test_outbound_sms(self):
        payload = {"from": "", "to": "", "text": "Hello world!"}
