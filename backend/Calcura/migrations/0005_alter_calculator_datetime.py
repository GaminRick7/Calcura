# Generated by Django 4.1.5 on 2023-03-29 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calcura', '0004_alter_calculator_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculator',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 29, 10, 23, 39, 242036)),
        ),
    ]