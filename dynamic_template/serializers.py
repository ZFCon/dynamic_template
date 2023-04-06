from rest_framework import serializers

from dynamic_template.models import EXAMPLE_SCHEMA
from dynamic_template.validators import JSONSchemaValidator


class RequestSerializer(serializers.Serializer):
    data = serializers.JSONField()

    def __init__(self, instance, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields["data"].validators.append(JSONSchemaValidator(EXAMPLE_SCHEMA))
