# Generated by Django 2.0 on 2019-06-30 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0003_remove_voucherrules_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefit',
            name='voucher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='voucher_benefit', to='voucher.Voucher'),
        ),
        migrations.AlterField(
            model_name='productrange',
            name='voucher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='voucher_range', to='voucher.Voucher'),
        ),
        migrations.AlterField(
            model_name='voucherrules',
            name='voucher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='voucher_rule', to='voucher.Voucher'),
        ),
    ]