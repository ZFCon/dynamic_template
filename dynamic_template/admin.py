from django.contrib import admin

from dynamic_template.models import Template, TemplateField


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(TemplateField)
class TemplateFieldAdmin(admin.ModelAdmin):
    readonly_fields = ("schema",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "template",
                    "type",
                    "is_choice_field",
                    "choices",
                    "schema",
                ),
            },
        ),
    )
