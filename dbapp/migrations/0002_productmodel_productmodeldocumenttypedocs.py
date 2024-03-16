# Generated by Django 5.0.3 on 2024-03-10 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dbapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductModel",
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
                ("model", models.CharField(blank=True, max_length=100, null=True)),
                ("link", models.CharField(blank=True, max_length=1000, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_models",
                        to="dbapp.brand",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductModelDocumentTypeDocs",
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
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("doc_link", models.CharField(blank=True, max_length=1000, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="document_type",
                        to="dbapp.productmodel",
                    ),
                ),
            ],
        ),
    ]
