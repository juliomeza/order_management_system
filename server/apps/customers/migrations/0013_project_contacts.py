# Generated by Django 5.1.5 on 2025-01-27 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0012_remove_project_carrier_remove_project_service_and_more'),
        ('logistics', '0012_remove_contact_contact_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contacts',
            field=models.ManyToManyField(blank=True, related_name='projects', to='logistics.contact'),
        ),
    ]
