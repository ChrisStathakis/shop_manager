# Generated by Django 2.0.7 on 2019-05-25 14:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sale', '0015_auto_20190520_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_expired',
            field=models.DateField(default=datetime.datetime(2019, 5, 25, 17, 18, 35, 225743), verbose_name='Ημερομηνία'),
        ),
    ]
