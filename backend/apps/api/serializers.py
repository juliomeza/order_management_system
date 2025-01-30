from rest_framework import serializers
from apps.orders.models import Order, OrderLine

class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = ['material', 'quantity', 'license_plate', 'serial_number', 
                 'lot', 'vendor_lot', 'notes']

class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['lookup_code_order', 'lookup_code_shipment', 'status', 
                 'order_type', 'order_class', 'project', 'warehouse', 
                 'contact', 'shipping_address', 'billing_address', 'carrier', 
                 'service_type', 'expected_delivery_date', 'notes', 'lines']

    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        order = Order.objects.create(**validated_data)
        
        for line_data in lines_data:
            OrderLine.objects.create(order=order, **line_data)
        
        return order