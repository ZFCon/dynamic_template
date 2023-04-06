# Generated by Django 4.1.7 on 2023-04-06 22:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dynamic_template", "0012_rename_outbondrequest_outbond"),
    ]

    operations = [
        migrations.CreateModel(
            name="OutbondRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.TextField()),
                ("data_before", models.JSONField()),
                (
                    "outbond",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dynamic_template.outbond",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]