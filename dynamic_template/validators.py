import jsonschema
from rest_framework.exceptions import ValidationError


class JSONSchemaValidator:
    def __init__(self, schema) -> None:
        self.schema = schema

    def __call__(self, value) -> None:
        try:
            jsonschema.validate(instance=value, schema=self.schema)
        except Exception as error:
            raise ValidationError(detail=error.message)
