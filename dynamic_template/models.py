from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from dynamic_template.abstracts import (
    TemplateFieldAbstract,
    TemplateFieldQuerySetAbstract,
)

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

    @property
    def schema(self) -> dict:
        fields_schema = {**self.fields.get_schema(), **self.nested_fields.get_schema()}
        fields_name = [field.name for field in self.fields.all()] + [
            field.name for field in self.nested_fields.all()
        ]

        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            # We could add more complex validation in the feature.
            "properties": fields_schema,
            # All fields are required for now just to simplify the project.
            "required": fields_name,
        }


class TemplateNestedField(TemplateFieldAbstract):
    template = models.ForeignKey(
        "dynamic_template.Template",
        on_delete=models.CASCADE,
        related_name="nested_fields",
    )

    objects = TemplateFieldQuerySetAbstract.as_manager()

    @property
    def type(self) -> str:
        return "object"

    @property
    def schema(self) -> dict:
        schema = super().schema
        schema[self.name] = {**self.fields.get_schema()}

        return schema

    class Meta:
        verbose_name = "Nested field"
        verbose_name_plural = "Nested fields"


class TemplateField(TemplateFieldAbstract):
    class Type(models.TextChoices):
        NUMBER = "integer", "Number"
        CHAR = "string", "Char"

    template = models.ForeignKey(
        "dynamic_template.Template", on_delete=models.CASCADE, related_name="fields"
    )
    nested = models.ForeignKey(
        "dynamic_template.TemplateNestedField",
        on_delete=models.CASCADE,
        null=True,
        related_name="fields",
    )
    type = models.CharField(max_length=50, choices=Type.choices, default=Type.CHAR)

    is_choice_field = models.BooleanField(default=False)
    # Array default type is CharField for easier convertation.
    choices = ArrayField(
        models.CharField(max_length=255),
        default=["example", "anotherexample"],
        help_text="Don't use unwanted spaces.",
    )

    objects = TemplateFieldQuerySetAbstract.as_manager()

    def save(self, *args, **kwargs) -> None:
        # When the object created with nested use the template id for nested.
        if not self.pk and self.nested:
            self.template_id = self.nested.template_id

        return super().save(*args, **kwargs)

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
        schema = super().schema

        if self.is_choice_field and self.type == self.Type.CHAR:
            schema["enum"] = self.choices
        elif self.is_choice_field and self.type == self.Type.NUMBER:
            schema["enum"] = [int(choice) for choice in self.choices]

        return schema

    class Meta:
        verbose_name = "Field"
        verbose_name_plural = "Fields"
