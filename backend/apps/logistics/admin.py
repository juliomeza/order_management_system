from django.contrib import admin
from .models import Address, Warehouse, Carrier, CarrierService

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_line_1', 'city', 'state', 'country', 'postal_code', 'entity_type', 'address_type')
    search_fields = ('address_line_1', 'city', 'state', 'country', 'postal_code')
    ordering = ('country', 'state', 'city')
    #list_filter = ('country', 'state', 'city', 'address_type')

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'lookup_code', 'address', 'status')
    search_fields = ('name', 'lookup_code', 'address__address_line_1')
    ordering = ('name',)
    #list_filter = ('status',)

@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ('name', 'lookup_code')
    search_fields = ('name', 'lookup_code')
    ordering = ('name',)

@admin.register(CarrierService)
class CarrierServiceAdmin(admin.ModelAdmin):
    @admin.display(description='SERVICE')
    def service_name(self, obj):
        return obj.name
    list_display = ('carrier', 'service_name', 'lookup_code')
    search_fields = ('name', 'lookup_code', 'carrier__name')
    ordering = ('carrier', 'name')
    #list_filter = ('carrier',)