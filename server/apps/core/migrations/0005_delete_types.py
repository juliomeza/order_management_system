# Generated by Django 5.1.5 on 2025-01-23 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_auditlogs_core_auditl_entity_1c2026_idx_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Types',
        ),
    ]
