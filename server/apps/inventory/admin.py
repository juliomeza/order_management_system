from django.contrib import admin
from .models import UOM, MaterialPriceHistory, Material, MaterialType, Inventory, InventorySerialNumber
from apps.core.admin import TimeStampedModelAdmin

@admin.register(UOM)
class UOMAdmin(TimeStampedModelAdmin):
    list_display = ('name', 'lookup_code', 'description', 'created_date')
    search_fields = ('name', 'lookup_code')
    ordering = ('name',)
    #list_filter = ('created_date',)

@admin.register(MaterialPriceHistory)
class MaterialPriceHistoryAdmin(TimeStampedModelAdmin):
    list_display = ('material', 'price', 'effective_date', 'end_date')
    search_fields = ('material__name', 'material__lookup_code')
    ordering = ('material', 'effective_date',)
    #list_filter = ('material__project', 'effective_date')

class MaterialPriceHistoryInline(admin.TabularInline):
    model = MaterialPriceHistory
    extra = 0
    fields = ('price', 'effective_date', 'end_date')
    can_delete = False

@admin.register(Material)
class MaterialAdmin(TimeStampedModelAdmin):
    list_display = ('name', 'lookup_code', 'status', 'type', 'uom', 'project', 'current_price')
    search_fields = ('name', 'lookup_code', 'project__name', 'status__name')
    ordering = ('name',)
    inlines = [MaterialPriceHistoryInline]
    #list_filter = ('status', 'project', 'uom')

@admin.register(MaterialType)
class MaterialTypeAdmin(TimeStampedModelAdmin):
    list_display = ('name', 'lookup_code', 'description')
    search_fields = ('name', 'lookup_code')
    ordering = ('name',)

@admin.register(Inventory)
class InventoryAdmin(TimeStampedModelAdmin):
    list_display = ('material', 'location', 'license_plate_id', 'quantity', 'project', 'warehouse')
    search_fields = ('material__name', 'warehouse__name', 'location', 'license_plate_id')
    ordering = ('project', 'warehouse', 'material', 'location', 'license_plate_id')
    #list_filter = ('warehouse', 'material', 'last_updated')

@admin.register(InventorySerialNumber)
class InventorySerialNumberAdmin(TimeStampedModelAdmin):
    list_display = ('license_plate', 'lookup_code', 'status')
    search_fields = ('lookup_code', 'license_plate__license_plate_id', 'status__name')
    ordering = ('license_plate', 'lookup_code',)
    #list_filter = ('status',)