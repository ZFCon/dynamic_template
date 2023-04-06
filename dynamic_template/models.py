from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from dynamic_template.abstracts import (
    TemplateFieldAbstract,
    TemplateFieldQuerySetAbstract,
)


class Template(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

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

    def data_map(self, data: dict, data_shape: str) -> dict:
        """Return a dict of the data but with the shape"""
        from django.template import Context, Template

        template = Template(data_shape)
        context = Context(data)

        return template.render(context)


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
    # We could implement more types in the feature in spirit them into class field.
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
    # TODO: Add validation array with pre defined types of validation.

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


class OutbondRequest(models.Model):
    template = models.ForeignKey(
        "dynamic_template.Template", on_delete=models.CASCADE, related_name="requests"
    )
    # We will only support Post request for now.
    url = models.URLField(max_length=255)

    EXAMPLE_DATA = """{
        "userId": {{userId}},
        "productId": {{eventData.productId}},
        "quantity": {{eventData.quantity}},
        "price": {{eventData.price}}
    }"""

    data_shape = models.TextField(
        default=EXAMPLE_DATA,
    )

    def __str__(self) -> str:
        return self.url

    def map_data(self, data):
        return self.template.data_map(data, self.data_shape)
