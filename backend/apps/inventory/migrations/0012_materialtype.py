# Generated by Django 5.1.5 on 2025-01-28 21:23

import apps.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_alter_inventoryserialnumber_lookup_code_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('lookup_code', models.CharField(max_length=50, unique=True, validators=[apps.core.validators.validate_lookup_code])),
                ('description', models.CharField(blank=True, max_length=100)),
                ('created_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['lookup_code'], name='inventory_m_lookup__bd6aa4_idx')],
            },
        ),
    ]
