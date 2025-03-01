# Generated by Django 5.1.5 on 2025-01-23 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0005_contact'),
        ('orders', '0009_alter_ordertype_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='logistics.contact'),
        ),
    ]
