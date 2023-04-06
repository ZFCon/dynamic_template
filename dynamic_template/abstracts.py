from django.db import models


class TemplateFieldAbstract(models.Model):
    template = models.ForeignKey("dynamic_template.Template", on_delete=models.CASCADE)
    name = models.CharField(max_length=55)

    class Meta:
        abstract = True

    @property
    def type(self) -> str:
        ...

    @property
    def schema(self) -> dict:
        return {
            "type": self.type,
        }

    def __str__(self) -> str:
        return f"{self.name}({self.type})"


class TemplateFieldQuerySetAbstract(models.QuerySet):
    def get_schema(self) -> dict:
        schema = {}
        for field in self:
            schema[field.name] = field.schema

        return schema
