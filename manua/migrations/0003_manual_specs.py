# Generated by Django 5.0.3 on 2024-03-22 11:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manua", "0002_brand_link_product_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="manual",
            name="specs",
            field=models.JSONField(blank=True, null=True),
        ),
    ]