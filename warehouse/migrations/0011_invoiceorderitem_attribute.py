# Generated by Django 2.0.7 on 2019-06-18 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0010_auto_20190525_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceorderitem',
            name='attribute',
            field=models.BooleanField(default=False),
        ),
    ]
