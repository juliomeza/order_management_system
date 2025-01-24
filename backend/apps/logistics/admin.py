from django.contrib import admin
from .models import Contact, Address, Warehouse, Carrier, CarrierService

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    def get_addresses(self, obj):
        return ", ".join([str(addr) for addr in obj.addresses.all()])
    get_addresses.short_description = 'Addresses'

    list_display = ['first_name', 'last_name', 'email', 'phone', 'get_addresses']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering = ['last_name', 'first_name']
    autocomplete_fields = ['addresses']
    #raw_id_fields = ['address']
    #list_filter = ['contact_type']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_line_1', 'city', 'state', 'postal_code', 'country', 'entity_type', 'address_type')
    search_fields = ('address_line_1', 'city', 'state', 'postal_code''country')
    ordering = ('address_line_1', 'city','state')
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