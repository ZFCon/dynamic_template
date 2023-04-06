from django.contrib import admin

from dynamic_template.models import (
    OutbondRequest,
    Template,
    TemplateField,
    TemplateNestedField,
)


class TemplateFieldInline(admin.StackedInline):
    model = TemplateField
    extra = 0
    min_num = 1
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


class OutbondRequestInline(admin.StackedInline):
    model = OutbondRequest
    extra = 0
    min_num = 1


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    inlines = (TemplateFieldInline, OutbondRequestInline)


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


class TemplateFieldForNestedInline(admin.StackedInline):
    model = TemplateField
    extra = 0
    min_num = 1
    readonly_fields = ("schema",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "nested",
                    "type",
                    "is_choice_field",
                    "choices",
                    "schema",
                ),
            },
        ),
    )


@admin.register(TemplateNestedField)
class TemplateFieldAdmin(admin.ModelAdmin):
    inlines = (TemplateFieldForNestedInline,)
    readonly_fields = ("schema",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "template",
                    "schema",
                ),
            },
        ),
    )
