from django.contrib import admin
from .models import Order, OrderClass

admin.site.register(Order)
admin.site.register(OrderClass)