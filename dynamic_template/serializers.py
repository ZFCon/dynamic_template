from rest_framework import serializers

from dynamic_template.models import OutbondRequest, Template
from dynamic_template.validators import JSONSchemaValidator


class RequestSerializer(serializers.Serializer):
    data = serializers.JSONField()

    def __init__(self, instance: Template, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields["data"].validators.append(JSONSchemaValidator(instance.schema))

    def to_representation(self, instance):
        return self.validated_data

    def create(self, validated_data):
        data = validated_data["data"]
        request = self.context["request"]

        for outbond in self.instance.requests.all():
            message = outbond.outbond(data)

            OutbondRequest.objects.create(
                outbond=outbond, user=request.user, data=message, data_before=data
            )

        return None
