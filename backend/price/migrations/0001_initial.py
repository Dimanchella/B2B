# Generated by Django 4.2.10 on 2024-03-30 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('characteristic', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='characteristic_price', to='catalog.characteristic', verbose_name='Характеристика')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='catalog.product', verbose_name='Номенклатура')),
            ],
            options={
                'verbose_name': 'Прайс',
                'verbose_name_plural': 'Прайс-листы',
            },
        ),
    ]

