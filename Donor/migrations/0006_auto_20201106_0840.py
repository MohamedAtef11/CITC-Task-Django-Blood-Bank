# Generated by Django 3.1.2 on 2020-11-06 08:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Donor', '0005_auto_20201104_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='BloodExpirationDate',
            field=models.DateField(default=datetime.datetime(2020, 12, 18, 8, 40, 5, 5243)),
        ),
    ]