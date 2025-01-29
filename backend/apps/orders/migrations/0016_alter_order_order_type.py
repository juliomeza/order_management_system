# Generated by Django 5.1.5 on 2025-01-29 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_remove_ordertype_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(blank=True, choices=[('INBOUND', 'Inbound'), ('OUTBOUND', 'Outbound')], help_text='INBOUND: Receiving inventory, OUTBOUND: Shipping to customers', max_length=8, null=True),
        ),
    ]
