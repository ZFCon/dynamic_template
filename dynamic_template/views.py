from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from dynamic_template.models import Template
from dynamic_template.serializers import RequestSerializer


class RequestAPIView(GenericAPIView):
    queryset = Template.objects.get_queryset()
    serializer_class = RequestSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
