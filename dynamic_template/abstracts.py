from django.db import models


class TemplateFieldAbstract(models.Model):
    template = models.ForeignKey("dynamic_template.Template", on_delete=models.CASCADE)
    name = models.CharField(max_length=55)

    class Meta:
        abstract = True

    @property
    def type(self) -> str:
        raise NotImplemented

    @property
    def schema(self) -> dict:
        raise NotImplemented

    def __str__(self) -> str:
        return f"{self.name}({self.type})"
