# -*- coding: utf-8 -*-
# Generated by Django 5.0.4 on 2024-08-12 12:43


from django.db import migrations, models
from django.apps import apps


def forwards(apps, schema_editor):
    Tag = apps.get_model("polls", "Tag")
    for tag in Tag.objects.all():
        tag.title = tag.title.upper()
        tag.save()


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0001_squashed_0004_alter_pizza_toppings"),
    ]

    operations = [
        migrations.CreateModel(
            name="PdfFileModel",
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
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                ("pdf", models.FileField(upload_to="pdfs")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RunPython(forwards),
    ]