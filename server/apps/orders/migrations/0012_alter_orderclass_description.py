# Generated by Django 5.1.5 on 2025-01-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_order_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderclass',
            name='description',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
