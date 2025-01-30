from django.urls import path
from .views import get_or_create_orders

urlpatterns = [
    path('orders/', get_or_create_orders, name="get-orders"),
]
