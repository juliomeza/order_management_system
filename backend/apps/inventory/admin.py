from django.contrib import admin
from .models import UOM, Material, Inventory, InventorySerialNumber

admin.site.register(UOM)
admin.site.register(Material)
admin.site.register(Inventory)
admin.site.register(InventorySerialNumber)