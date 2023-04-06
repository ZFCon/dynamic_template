from django.contrib import admin

from dynamic_template.models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass
