# Generated by Django 5.1.5 on 2025-03-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_rename_lenght_products_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='colors',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='sizes',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
