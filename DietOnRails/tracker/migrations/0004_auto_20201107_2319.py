# Generated by Django 3.1.2 on 2020-11-08 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20201107_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodgroup',
            name='trans_fat',
            field=models.FloatField(blank=True, help_text='Units: g', null=True),
        ),
        migrations.AddField(
            model_name='savedfood',
            name='trans_fat',
            field=models.FloatField(blank=True, help_text='Units: g', null=True),
        ),
    ]