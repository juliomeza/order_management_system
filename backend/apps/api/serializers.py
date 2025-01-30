from rest_framework import serializers
from apps.orders.models import Order, OrderLine
import logging

logger = logging.getLogger('custom_logger')

class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = ['material', 'quantity', 'license_plate', 'serial_number', 
                 'lot', 'vendor_lot', 'notes']

class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ['lookup_code_order', 'lookup_code_shipment', 'status', 
                 'order_type', 'order_class', 'project', 'warehouse', 
                 'contact', 'shipping_address', 'billing_address', 'carrier', 
                 'service_type', 'expected_delivery_date', 'notes', 'lines']
    
    def validate(self, data):
        # Verificar que hay al menos una línea
        if not data.get('lines') or len(data.get('lines')) == 0:
            logger.warning("Validation failed: No order lines provided.")
            raise serializers.ValidationError(
                {"lines": "At least one order line is required"}
            )
        return data

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        order = Order.objects.create(**validated_data)
        
        for line_data in lines_data:
            OrderLine.objects.create(order=order, **line_data)
        
        logger.info(f"Order created successfully: {order.lookup_code_order} with {len(lines_data)} lines.")
        return order