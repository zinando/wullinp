# Generated by Django 5.1.5 on 2025-03-04 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_address_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='lga',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='lga_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
