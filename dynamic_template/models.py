from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from dynamic_template.abstracts import TemplateFieldAbstract

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
        default=EXAMPLE_SCHEMA,
        help_text="To learn more about json-schema visit http://json-schema.org",
    )


class TemplateField(TemplateFieldAbstract):
    class Type(models.TextChoices):
        NUMBER = "integer", "Number"
        CHAR = "string", "Char"

    template = models.ForeignKey(
        "dynamic_template.Template", on_delete=models.CASCADE, related_name="fields"
    )
    type = models.CharField(max_length=50, choices=Type.choices, default=Type.CHAR)

    is_choice_field = models.BooleanField(default=False)
    # Array default type is CharField for easier convertation.
    choices = ArrayField(
        models.CharField(max_length=255),
        default=["example", "anotherexample"],
        help_text="Don't use unwanted spaces.",
    )

    def clean(self) -> None:
        if self.is_choice_field and self.type == self.Type.NUMBER:
            try:
                [int(choice) for choice in self.choices]
            except ValueError:
                raise ValidationError(
                    "Make sure choices are the same type(Number) as type field with no spaces."
                )

        return super().clean()

    @property
    def schema(self) -> dict:
        schema = {
            "type": self.type,
        }

        if self.is_choice_field and self.type == self.Type.CHAR:
            schema["enum"] = self.choices
        elif self.is_choice_field and self.type == self.Type.NUMBER:
            schema["enum"] = [int(choice) for choice in self.choices]

        return schema
