from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dynamic_template.factories import TemplateFactory


class RequestTest(APITestCase):
    def setUp(self) -> None:
        self.template = TemplateFactory.create()

    def test_create_event(self):
        url = reverse("dynamic_template:requests", args=(self.template.pk,))
        data = {
            "data": {
                "userId": 123,
                "eventType": "purchase",
                "eventData": {"productId": 456, "quantity": 2, "price": 100},
            }
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)
