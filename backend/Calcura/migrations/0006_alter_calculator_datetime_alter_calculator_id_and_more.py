# Generated by Django 4.1.5 on 2023-03-29 14:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Calcura', '0005_alter_calculator_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculator',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 29, 10, 45, 39, 888120)),
        ),
        migrations.AlterField(
            model_name='calculator',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='calculator',
            name='title',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='calculator',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]