# Generated by Django 2.0.7 on 2019-06-18 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_auto_20190614_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='qty_add',
            field=models.IntegerField(default=0.0, help_text='we use this for manual add.', verbose_name='Υπόλοιπο'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='qty_remove',
            field=models.IntegerField(default=0.0, help_text='System use it only if warehouse transations', verbose_name='Qty Remove'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='qty',
            field=models.IntegerField(default=0, verbose_name='Ποσότητα'),
        ),
    ]
