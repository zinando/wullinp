# Generated by Django 5.1.5 on 2025-03-13 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0005_mysavedproduct_delete_flag_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysavedproduct',
            name='shipping_cost',
            field=models.FloatField(default=2000),
        ),
    ]
