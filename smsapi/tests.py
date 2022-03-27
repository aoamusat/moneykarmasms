import environ
import base64
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import Client
from django.core.cache import cache
import requests as Http

env = environ.Env()
environ.Env.read_env()

# Create your tests here.
class AuthenticationClass(APITestCase):
    def setUp(self):
        self.username = "azr1"
        self.password = "20S0KPNOIM"
        self.base_url = f"{env('APP_URL')}:{env('APP_PORT')}/"
        self.token = base64.b64encode(
            f"{self.username}:{self.password}".encode("utf-8")
        ).decode("utf-8")
        cache.set("TEST", "Testing MoneyKarma", timeout=3600 * 4)
        self.Http = Http
        self.text = "Hello World!"
        self.to = "4924195509196"
        self.frm = "492419550912"

    def test_valid_authentication(self):
        response = self.Http.get(
            self.base_url, headers={"Authorization": f"Basic {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_authentication(self):
        response = self.Http.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_inbound_sms(self):
        payload = {
            "from": self.frm,
            "to": self.to,
            "text": self.text,
        }
        response = self.Http.post(
            self.base_url + "api/v1/inbound/sms",
            data=payload,
            headers={"Authorization": f"Basic {self.token}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_outbound_sms(self):
        payload = {
            "from": self.frm,
            "to": self.to,
            "text": self.text,
        }
        response = self.Http.post(
            self.base_url + "api/v1/outbound/sms",
            data=payload,
            headers={"Authorization": f"Basic {self.token}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_inbound_sms(self):
        payload = {"from": "", "to": "", "text": ""}
        response = self.Http.post(
            self.base_url + "api/v1/inbound/sms",
            data=payload,
            headers={"Authorization": f"Basic {self.token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_outbound_sms(self):
        payload = {
            "from": "",
            "to": "",
            "text": "Hello world!",
        }

        response = self.Http.post(
            self.base_url + "api/v1/outbound/sms",
            data=payload,
            headers={"Authorization": f"Basic {self.token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_caching(self):
        self.assertNotEqual(None, cache.get("TEST"))

    def test_requests(self):
        headers = {"Authorization": f"Basic {self.token}"}
        response = Http.get(self.base_url, headers=headers, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        cache.delete("TEST")
