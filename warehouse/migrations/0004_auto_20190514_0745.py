# Generated by Django 2.0.7 on 2019-05-14 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_auto_20190511_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('notes', models.TextField()),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('active', models.BooleanField(default=True)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='employee',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='Υπόλοιπο'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='occupation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='warehouse.Occupation', verbose_name='Επάγγελμα'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(blank=True, max_length=10, verbose_name='Κινητό'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone1',
            field=models.CharField(blank=True, max_length=10, verbose_name='Σταθερό'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='title',
            field=models.CharField(max_length=64, unique=True, verbose_name='Ονομασία'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='vacation_days',
            field=models.IntegerField(default=0, verbose_name='Υμέρες Άδειας'),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='Υπόλοιπο'),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Ονομασία'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='category',
            field=models.CharField(choices=[('1', 'Μισθός'), ('2', 'ΙΚΑ'), ('3', 'ΑΣΦΑΛΙΣΤΙΚΕΣ ΕΙΣΦΟΡΕΣ'), ('4', 'ΗΜΕΡΟΜΗΣΘΙΟ'), ('5', 'ΕΡΓΟΣΗΜΟ'), ('6', 'ΔΩΡΟ')], default='1', max_length=1, verbose_name='Κατηγορία'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_invoices', to='warehouse.Employee', verbose_name='Υπάλληλος'),
        ),
        migrations.AddField(
            model_name='genericexpense',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.GenericPerson', verbose_name="Εταιρία/'Ατομο"),
        ),
    ]
