# Generated by Django 5.1.5 on 2025-02-05 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='_static/images/vendor_logos/'),
        ),
    ]
