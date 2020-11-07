# Generated by Django 3.1.2 on 2020-11-06 23:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Donor', '0007_auto_20201106_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='id_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='donor',
            name='BloodExpirationDate',
            field=models.DateField(default=datetime.datetime(2020, 12, 18, 23, 19, 50, 491247)),
        ),
    ]
