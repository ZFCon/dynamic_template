from django.db import models

EXAMPLE_SCHEMA = {
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

EXAMPLE_DATA = {
    "userId": 123,
    "eventType": "purchase",
    "eventData": {"productId": 456, "quantity": 2, "price": 100},
}


class Template(models.Model):
    data_format = models.JSONField(
        help_text="You should use http://json-schema.org to create the format for the expected data."
    )
