# Generated by Django 2.0 on 2019-05-11 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_auto_20190509_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billcategory',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='Υπόλοιπο'),
        ),
        migrations.AlterField(
            model_name='billcategory',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Τίτλος'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bills', to='warehouse.BillCategory', verbose_name='Λογαριασμός'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='occupation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='warehouse.Occupation', verbose_name='Occupation'),
        ),
    ]
