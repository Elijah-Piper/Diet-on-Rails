# Generated by Django 3.1.2 on 2020-11-08 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_savedfood_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savedfood',
            old_name='brand_name',
            new_name='brand',
        ),
    ]
