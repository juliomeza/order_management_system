from django.contrib import admin
from .models import Order, OrderClass, OrderLine

admin.site.register(Order)
admin.site.register(OrderClass)
admin.site.register(OrderLine)