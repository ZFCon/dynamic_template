from django.contrib import admin

from dynamic_template.models import (
    Outbond,
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


class OutbondInline(admin.StackedInline):
    model = Outbond
    extra = 0
    min_num = 1


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    readonly_fields = ("schema",)
    inlines = (TemplateFieldInline, OutbondInline)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "schema",
                ),
            },
        ),
    )


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


@admin.register(OutbondRequest)
class OutbondRequestAdmin(admin.ModelAdmin):
    pass
