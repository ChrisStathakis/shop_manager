# Generated by Django 2.0.7 on 2019-05-09 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_settings', '0001_initial'),
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Friendly ID')),
                ('title', models.CharField(max_length=150, verbose_name='Τίτλος')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('date_expired', models.DateField(default=django.utils.timezone.now, verbose_name='Ημερομηνία')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Αξία')),
                ('taxes', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Φόρος')),
                ('paid_value', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Πληρωτέα Αξία')),
                ('final_value', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Αξία')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Έκπτωση')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Πληρωμένο')),
                ('printed', models.BooleanField(default=False, verbose_name='Εκτυπωμένο')),
            ],
            options={
                'verbose_name': 'Εντολή Πληρωμής',
                'verbose_name_plural': '3. Εντολή Πληρωμής Γενικών Εξόδων',
                'ordering': ['is_paid', '-date_expired'],
            },
        ),
        migrations.CreateModel(
            name='GenericExpenseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=150, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
            ],
            options={
                'verbose_name': 'Έξοδο',
                'verbose_name_plural': '7. Γενικά Έξοδα',
            },
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='date_expired',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Ημερομηνία'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Έκπτωση'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='final_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Αξία'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Πληρωμένο'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='paid_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Πληρωτέα Αξία'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='site_settings.PaymentMethod', verbose_name='Τρόπος Πληρωμής'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='printed',
            field=models.BooleanField(default=False, verbose_name='Εκτυπωμένο'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='taxes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Φόρος'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Τίτλος'),
        ),
        migrations.AlterField(
            model_name='billinvoice',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Αξία'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='additional_value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Επιπλέον Κόστος'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='clean_value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Καθαρή Αξία'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date_expired',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Ημερομηνία'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Έκπτωση'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='final_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Αξία'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Πληρωμένο'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='order_type',
            field=models.CharField(choices=[('1', 'Τιμολόγιο - Δελτίο Αποστολής'), ('2', 'Τιμολόγιο'), ('3', 'Δελτίο Απόστολης'), ('4', 'Εισαγωγή Αποθήκης'), ('5', 'Εξαγωγή Αποθήκης')], default=1, max_length=1, verbose_name='Είδος'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paid_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Πληρωτέα Αξία'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paycheck',
            field=models.ManyToManyField(to='catalogue.VendorPaycheck', verbose_name='Πληρωμές'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='site_settings.PaymentMethod', verbose_name='Τρόπος Πληρωμής'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='printed',
            field=models.BooleanField(default=False, verbose_name='Εκτυπωμένο'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='taxes',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Φόρος'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='taxes_modifier',
            field=models.CharField(choices=[('1', 13), ('2', 23), ('3', 24), ('4', 0)], default='1', max_length=1, verbose_name='ΦΠΑ'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Τίτλος'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Αξία'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor_orders', to='catalogue.Vendor', verbose_name='Προμηθευτής'),
        ),
        migrations.AlterField(
            model_name='invoiceorderitem',
            name='discount_value',
            field=models.IntegerField(default=0, verbose_name='Έκπτωση %'),
        ),
        migrations.AlterField(
            model_name='invoiceorderitem',
            name='qty',
            field=models.PositiveIntegerField(default=1, verbose_name='Ποσότητα'),
        ),
        migrations.AlterField(
            model_name='invoiceorderitem',
            name='total_clean_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Συνολική Καθαρή Αξία'),
        ),
        migrations.AlterField(
            model_name='invoiceorderitem',
            name='total_final_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14, verbose_name='Συνολίκή Αξία'),
        ),
        migrations.AlterField(
            model_name='invoiceorderitem',
            name='unit',
            field=models.CharField(choices=[('1', 'Τεμάχια'), ('2', 'Κιλά'), ('3', 'Κιβώτια')], default='1', max_length=1, verbose_name='Μονάδα Μέτρησης'),
        ),
        migrations.AlterField(
            model_name='invoiceorderitem',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Αξία'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='date_expired',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Ημερομηνία'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Έκπτωση'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='final_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Αξία'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Πληρωμένο'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='paid_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Πληρωτέα Αξία'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='site_settings.PaymentMethod', verbose_name='Τρόπος Πληρωμής'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='printed',
            field=models.BooleanField(default=False, verbose_name='Εκτυπωμένο'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='taxes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Φόρος'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Τίτλος'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Αξία'),
        ),
        migrations.AddField(
            model_name='genericexpense',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expenses', to='warehouse.GenericExpenseCategory'),
        ),
        migrations.AddField(
            model_name='genericexpense',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='site_settings.PaymentMethod', verbose_name='Τρόπος Πληρωμής'),
        ),
        migrations.AddField(
            model_name='genericexpense',
            name='user_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]