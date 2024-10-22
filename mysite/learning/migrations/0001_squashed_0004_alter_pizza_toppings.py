# -*- coding: utf-8 -*-
# Generated by Django 5.0.4 on 2024-08-12 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("learning", "0001_initial"),
        ("learning", "0002_topping_pizza"),
        ("learning", "0003_restaurant"),
        ("learning", "0004_alter_pizza_toppings"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TablespaceExample",
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
                (
                    "name",
                    models.CharField(
                        db_index=True, db_tablespace="indexes", max_length=30
                    ),
                ),
                ("data", models.CharField(db_index=True, max_length=255)),
                ("shortcut", models.CharField(max_length=7)),
                (
                    "edges",
                    models.ManyToManyField(
                        db_tablespace="indexes", to="learning.tablespaceexample"
                    ),
                ),
            ],
            options={
                "db_tablespace": "tables",
                "indexes": [
                    models.Index(
                        db_tablespace="other_indexes",
                        fields=["shortcut"],
                        name="learning_ta_shortcu_8c2341_idx",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="Topping",
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
                ("name", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Pizza",
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
                ("name", models.CharField(max_length=50)),
                (
                    "toppings",
                    models.ManyToManyField(related_name="pizza", to="learning.topping"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Restaurant",
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
                (
                    "best_pizza",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="championed_by",
                        to="learning.pizza",
                    ),
                ),
                (
                    "pizzas",
                    models.ManyToManyField(
                        related_name="restaurants", to="learning.pizza"
                    ),
                ),
            ],
        ),
    ]
