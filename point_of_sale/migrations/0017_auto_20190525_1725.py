# Generated by Django 2.0.7 on 2019-05-25 14:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sale', '0016_auto_20190525_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_expired',
            field=models.DateField(default=datetime.date(2019, 5, 25), verbose_name='Ημερομηνία'),
        ),
    ]
