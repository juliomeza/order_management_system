from django.urls import path
from .views import get_or_create_orders, get_or_create_order_lines

urlpatterns = [
    path('orders/', get_or_create_orders, name="get-orders"),
    path('order-lines/', get_or_create_order_lines, name="get-order-lines"),
]
