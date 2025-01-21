from django.contrib import admin
from .models import Address, Warehouse, Carrier, CarrierService

admin.site.register(Address)
admin.site.register(Warehouse)
admin.site.register(Carrier)
admin.site.register(CarrierService)