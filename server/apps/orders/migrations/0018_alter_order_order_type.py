# Generated by Django 5.1.5 on 2025-01-29 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_order_order_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.ForeignKey(help_text='INBOUND: Receiving inventory, OUTBOUND: Shipping to customers', on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='orders.ordertype'),
        ),
    ]
