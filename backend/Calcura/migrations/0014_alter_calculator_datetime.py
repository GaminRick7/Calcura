# Generated by Django 4.1.5 on 2023-03-29 19:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calcura', '0013_rename_two_messageroom_user2_remove_messageroom_one_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculator',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 29, 15, 37, 17, 93529)),
        ),
    ]