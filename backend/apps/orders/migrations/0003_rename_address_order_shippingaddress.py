# Generated by Django 5.1.5 on 2025-01-22 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_carrier_alter_order_servicetype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='shippingAddress',
        ),
    ]
