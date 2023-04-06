from rest_framework import serializers

from dynamic_template.models import Template
from dynamic_template.validators import JSONSchemaValidator


class RequestSerializer(serializers.Serializer):
    data = serializers.JSONField()

    def __init__(self, instance: Template, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields["data"].validators.append(JSONSchemaValidator(instance.schema))

    def to_representation(self, instance):
        return self.validated_data

    def create(self, validated_data):
        for outbond_request in self.instance.requests.all():
            response = outbond_request.outbond(validated_data["data"])
            if not response:
                self.validated_data[
                    outbond_request.url
                ] = "Something went wrong calling it."

        return None
