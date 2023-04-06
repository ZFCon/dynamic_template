import factory

from dynamic_template.models import Template, TemplateField, TemplateNestedField


class TemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Template
        django_get_or_create = ("name",)

    name = "Tema"


class TemplateFieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemplateField
        django_get_or_create = ("name",)

    name = "Tema"


class TemplateNestedFieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemplateNestedField
        django_get_or_create = ("name",)

    name = "Tema"
