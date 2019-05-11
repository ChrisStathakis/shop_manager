# Generated by Django 2.0.7 on 2019-05-09 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20190418_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.WarehouseCategory', verbose_name='Κατηγορία Αποθήκης'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category_site',
            field=models.ManyToManyField(blank=True, null=True, to='catalogue.Category', verbose_name='Κατηγορία Site'),
        ),
        migrations.AlterField(
            model_name='product',
            name='featured_product',
            field=models.BooleanField(default=False, verbose_name='Εμφάνιση Πρώτη Σελίδα'),
        ),
        migrations.AlterField(
            model_name='product',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Τιμή Πώλησης'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_offer',
            field=models.BooleanField(default=False, verbose_name='Προσφορά'),
        ),
        migrations.AlterField(
            model_name='product',
            name='measure_unit',
            field=models.CharField(blank=True, choices=[('1', 'Τεμάχια'), ('2', 'Κιλά'), ('3', 'Κιβώτια')], default='1', max_length=1, null=True, verbose_name='Μονάδα Μέτρησης'),
        ),
        migrations.AlterField(
            model_name='product',
            name='order_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Κωδικός Τιμολογίου'),
        ),
        migrations.AlterField(
            model_name='product',
            name='order_discount',
            field=models.IntegerField(default=0, verbose_name="'Έκπτωση Τιμολογίου"),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Αρχική Τιμή'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_buy',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Αξία Αγοράς'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Εκπτωτική Τιμή'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.ProductClass', verbose_name='Είδος'),
        ),
        migrations.AlterField(
            model_name='product',
            name='qty_measure',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=5, verbose_name='Ποσότητα Ανά Τεμάχιο'),
        ),
        migrations.AlterField(
            model_name='product',
            name='safe_stock',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Όριο αποθέματος'),
        ),
        migrations.AlterField(
            model_name='productclass',
            name='have_attribute',
            field=models.BooleanField(default=False, verbose_name='Μεγεθολόγιο'),
        ),
        migrations.AlterField(
            model_name='productclass',
            name='have_transcations',
            field=models.BooleanField(default=True, verbose_name='Υποστηρίζει συναλλαγές'),
        ),
        migrations.AlterField(
            model_name='productclass',
            name='is_service',
            field=models.BooleanField(default=False, verbose_name='Υπηρεσία'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Κατάσταση'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='address',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Διεύθυνση'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Πόλη'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Σημειώσεις'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Κινητό'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone1',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Σταθερό'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='taxes_modifier',
            field=models.CharField(choices=[('1', 13), ('2', 23), ('3', 24), ('4', 0)], default='3', max_length=1, verbose_name='ΦΠΑ'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='title',
            field=models.CharField(max_length=70, unique=True, verbose_name='Ονομασία'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vat',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='ΑΦΜ'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vat_city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ΔΟΥ'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='zipcode',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='ΤΚ'),
        ),
    ]
