# Generated by Django 4.1.5 on 2023-03-30 00:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatSystem', '0006_alter_messages_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 29, 20, 28, 32, 335907)),
        ),
    ]