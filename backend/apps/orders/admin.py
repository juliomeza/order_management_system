from django.contrib import admin
from .models import Order, OrderClass, OrderType, OrderLine

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    @admin.display(description='ORDER', ordering='lookup_code_order')
    def order(self, obj):
        return obj.lookup_code_order
    list_display = ('project', 'order_type', 'warehouse', 'order', 'status', 'carrier', 'expected_delivery_date')
    search_fields = ('lookup_code_order', 'lookup_code_shipment', 'project__name', 'warehouse__name', 'carrier__name')
    ordering = ('project', 'order_type', 'warehouse', 'lookup_code_order',)
    #list_filter = ('order_type', 'status', 'project', 'warehouse', 'carrier')

@admin.register(OrderClass)
class OrderClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'description')
    search_fields = ('class_name',)
    ordering = ('class_name',)
    #list_filter = ('is_active',)

@admin.register(OrderType)
class OrderTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'description')
    search_fields = ('type_name',)
    ordering = ('type_name',)
    #list_filter = ('is_active',)

@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'material', 'quantity', 'license_plate', 'serial_number', 'lot', 'vendor_lot')
    search_fields = ('order__lookup_code_order', 'material__name', 'license_plate__license_plate_id', 'serial_number__lookup_code')
    ordering = ('order', 'material',)
    #list_filter = ('material',)