# Generated by Django 4.1 on 2023-04-11 12:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatSystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 11, 8, 19, 7, 155725)),
        ),
    ]