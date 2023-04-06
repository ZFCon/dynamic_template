from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dynamic_template.factories import (
    TemplateFactory,
    TemplateFieldFactory,
    TemplateNestedFieldFactory,
)
from dynamic_template.models import OutbondRequest, TemplateField


class RequestTest(APITestCase):
    def setUp(self) -> None:
        self.template = TemplateFactory.create()
        self.outbond_request = OutbondRequest.objects.create(
            template=self.template, url="https://inventory.example.com/api/update"
        )
        TemplateFieldFactory.create(
            template=self.template, name="userId", type=TemplateField.Type.NUMBER
        )
        TemplateFieldFactory.create(
            template=self.template,
            name="userId",
            type=TemplateField.Type.NUMBER,
            is_choice_field=True,
            choices=["purchase"],
        )
        nested_field = TemplateNestedFieldFactory.create(
            template=self.template, name="eventData"
        )
        TemplateFieldFactory.create(
            nested=nested_field, name="productId", type=TemplateField.Type.NUMBER
        )
        TemplateFieldFactory.create(
            nested=nested_field, name="quantity", type=TemplateField.Type.NUMBER
        )
        TemplateFieldFactory.create(
            nested=nested_field, name="price", type=TemplateField.Type.NUMBER
        )

    def test_create_event(self):
        url = reverse("dynamic_template:requests", args=(self.template.pk,))
        valid_data = {
            "data": {
                "userId": 123,
                "eventType": "purchase",
                "eventData": {"productId": 456, "quantity": 2, "price": 100},
            }
        }
        response = self.client.post(url, valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data["data"], valid_data["data"])
        self.assertIsNotNone(response.data.get(self.outbond_request.url))

        invalid_data = {
            "data": {
                "userId": "123",
                "eventType": "purchase",
                "eventData": {"productId": 456, "quantity": 2, "price": 100},
            }
        }
        response = self.client.post(url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data.get(self.outbond_request.url))
