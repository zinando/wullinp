# Generated by Django 5.1.5 on 2025-02-08 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productcategory_options_productcategory_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productcategory',
            old_name='title',
            new_name='name',
        ),
    ]
