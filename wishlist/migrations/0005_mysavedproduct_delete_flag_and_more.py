# Generated by Django 5.1.5 on 2025-03-12 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0004_donators_amount_donators_personal_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysavedproduct',
            name='delete_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mysavedproduct',
            name='shipping_info',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
