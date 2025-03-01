# Generated by Django 5.1.5 on 2025-01-28 15:59

import apps.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0013_alter_contact_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrier',
            name='lookup_code',
            field=models.CharField(max_length=50, unique=True, validators=[apps.core.validators.validate_lookup_code]),
        ),
        migrations.AlterField(
            model_name='carrierservice',
            name='lookup_code',
            field=models.CharField(max_length=50, unique=True, validators=[apps.core.validators.validate_lookup_code]),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='lookup_code',
            field=models.CharField(max_length=50, unique=True, validators=[apps.core.validators.validate_lookup_code]),
        ),
    ]
