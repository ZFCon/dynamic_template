import factory

from dynamic_template.models import Template


class TemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Template
        django_get_or_create = ("data_format",)

    data_format = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "userId": {
                "type": "integer",
                "minimum": 1,
            },
            "eventType": {
                "type": "string",
                "enum": ["purchase"],
            },
            "eventData": {
                "type": "object",
                "properties": {
                    "productId": {
                        "type": "integer",
                        "minimum": 1,
                    },
                    "quantity": {
                        "type": "integer",
                        "minimum": 1,
                    },
                    "price": {
                        "type": "integer",
                        "minimum": 1,
                    },
                },
            },
        },
        "required": ["userId", "eventType", "eventData"],
    }
