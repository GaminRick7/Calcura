# Generated by Django 4.1.5 on 2023-03-29 15:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Calcura', '0006_alter_calculator_datetime_alter_calculator_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculator',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 29, 11, 45, 2, 137934)),
        ),
        migrations.AlterField(
            model_name='calculator',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]