# Generated by Django 5.1.5 on 2025-01-21 20:16

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_initial'),
        ('customers', '0002_initial'),
        ('logistics', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('lookupCode', models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(max_length=50)),
                ('isSerialized', models.BooleanField(default=False)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('createdByUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('modifiedByUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materials', to='customers.project')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materials', to='core.status')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(max_length=50)),
                ('licensePlateID', models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('licensePlate', models.CharField(max_length=50)),
                ('lot', models.CharField(blank=True, max_length=50)),
                ('vendorLot', models.CharField(blank=True, max_length=50)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
                ('createdByUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('modifiedByUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventories', to='customers.project')),
                ('updatedByUser', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory_updates', to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventories', to='logistics.warehouse')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventories', to='inventory.material')),
            ],
            options={
                'verbose_name_plural': 'Inventories',
            },
        ),
        migrations.CreateModel(
            name='UOM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('lookupCode', models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('description', models.TextField(blank=True)),
                ('createdByUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('modifiedByUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Unit of Measure',
                'verbose_name_plural': 'Units of Measure',
            },
        ),
        migrations.AddField(
            model_name='material',
            name='uom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materials', to='inventory.uom'),
        ),
        migrations.CreateModel(
            name='InventorySerialNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('modifiedDate', models.DateTimeField(auto_now=True)),
                ('lookupCode', models.CharField(help_text='Serial number', max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('notes', models.TextField(blank=True)),
                ('createdByUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('licensePlate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='serial_numbers', to='inventory.inventory')),
                ('modifiedByUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='serial_numbers', to='core.status')),
            ],
            options={
                'indexes': [models.Index(fields=['lookupCode'], name='inventory_i_lookupC_e0a72f_idx'), models.Index(fields=['licensePlate'], name='inventory_i_license_db47d1_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='inventory',
            index=models.Index(fields=['project', 'warehouse', 'material'], name='inventory_i_project_481257_idx'),
        ),
        migrations.AddIndex(
            model_name='inventory',
            index=models.Index(fields=['licensePlateID'], name='inventory_i_license_54c5e7_idx'),
        ),
        migrations.AddIndex(
            model_name='inventory',
            index=models.Index(fields=['location'], name='inventory_i_locatio_e4ba1b_idx'),
        ),
        migrations.AddIndex(
            model_name='uom',
            index=models.Index(fields=['lookupCode'], name='inventory_u_lookupC_3b594e_idx'),
        ),
        migrations.AddIndex(
            model_name='material',
            index=models.Index(fields=['project', 'status'], name='inventory_m_project_8e6962_idx'),
        ),
        migrations.AddIndex(
            model_name='material',
            index=models.Index(fields=['lookupCode'], name='inventory_m_lookupC_15dd9b_idx'),
        ),
    ]
