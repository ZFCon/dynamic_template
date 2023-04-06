from rest_framework import serializers

from dynamic_template.models import Template
from dynamic_template.validators import JSONSchemaValidator


class RequestSerializer(serializers.Serializer):
    data = serializers.JSONField()

    def get_data(self, object):
        return "gg"

    def __init__(self, instance: Template, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields["data"].validators.append(JSONSchemaValidator(instance.data_format))

    def to_representation(self, instance):
        return self.initial_data
