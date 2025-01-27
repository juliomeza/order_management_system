from django.contrib import admin
from .models import UOM, Material, Inventory, InventorySerialNumber
from apps.core.admin import TimeStampedModelAdmin

@admin.register(UOM)
class UOMAdmin(TimeStampedModelAdmin):
    list_display = ('name', 'lookup_code', 'description', 'created_date')
    search_fields = ('name', 'lookup_code')
    ordering = ('name',)
    #list_filter = ('created_date',)

@admin.register(Material)
class MaterialAdmin(TimeStampedModelAdmin):
    list_display = ('name', 'lookup_code', 'status', 'type', 'price', 'uom', 'project')
    search_fields = ('name', 'lookup_code', 'project__name', 'status__name')
    ordering = ('name',)
    #list_filter = ('status', 'project', 'uom')

@admin.register(Inventory)
class InventoryAdmin(TimeStampedModelAdmin):
    list_display = ('project', 'warehouse', 'material', 'location', 'license_plate_id', 'quantity', 'last_updated')
    search_fields = ('material__name', 'warehouse__name', 'location', 'license_plate_id')
    ordering = ('project', 'warehouse', 'material', 'location', 'license_plate_id')
    #list_filter = ('warehouse', 'material', 'last_updated')

@admin.register(InventorySerialNumber)
class InventorySerialNumberAdmin(TimeStampedModelAdmin):
    list_display = ('license_plate', 'lookup_code', 'status')
    search_fields = ('lookup_code', 'license_plate__license_plate_id', 'status__name')
    ordering = ('license_plate', 'lookup_code',)
    #list_filter = ('status',)