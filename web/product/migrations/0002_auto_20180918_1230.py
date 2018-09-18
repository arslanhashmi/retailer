# Generated by Django 2.1.1 on 2018-09-18 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliveryservice',
            options={'verbose_name': 'delivery service', 'verbose_name_plural': 'delivery services'},
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='product.DeliveryService'),
        ),
    ]