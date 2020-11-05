# Generated by Django 3.1.2 on 2020-11-05 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('serving_weight', models.IntegerField()),
                ('calories', models.IntegerField()),
                ('total_fat', models.IntegerField()),
                ('saturated_fat', models.IntegerField()),
                ('cholesterol', models.IntegerField()),
                ('sodium', models.IntegerField()),
                ('total_carbs', models.IntegerField()),
                ('fiber', models.IntegerField()),
                ('sugars', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('potassium', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FoodLog',
            fields=[
                ('foodgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='tracker.foodgroup')),
                ('date', models.DateField()),
                ('identifier', models.CharField(max_length=60, primary_key=True, serialize=False)),
            ],
            bases=('tracker.foodgroup',),
        ),
        migrations.CreateModel(
            name='SavedFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('brand_name', models.CharField(max_length=60)),
                ('serving_qty', models.FloatField()),
                ('serving_unit', models.CharField(max_length=20)),
                ('serving_weight', models.IntegerField()),
                ('calories', models.IntegerField()),
                ('total_fat', models.IntegerField()),
                ('saturated_fat', models.IntegerField()),
                ('cholesterol', models.IntegerField()),
                ('sodium', models.IntegerField()),
                ('total_carbs', models.IntegerField()),
                ('fiber', models.IntegerField()),
                ('sugars', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('potassium', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_foods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='foodgroup',
            name='grouped_foods',
            field=models.ManyToManyField(related_name='foods', to='tracker.SavedFood'),
        ),
        migrations.AddField(
            model_name='foodgroup',
            name='grouped_groups',
            field=models.ManyToManyField(related_name='_foodgroup_grouped_groups_+', to='tracker.FoodGroup'),
        ),
        migrations.AddField(
            model_name='foodgroup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grouped_foods', to=settings.AUTH_USER_MODEL),
        ),
    ]
