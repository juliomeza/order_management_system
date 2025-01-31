from rest_framework import serializers
from apps.orders.models import Order, OrderLine
import logging
from django.db import transaction

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
        user = self.context['request'].user  # Get authenticated user

        # ✅ Validate that the selected project belongs to the user
        if data["project"].customer != user.project.customer:
            raise serializers.ValidationError({"project": "You can only create orders for your assigned customer."})

        # ✅ Validate materials belong to user's project
        for line in data.get("lines", []):
            if line["material"].project != user.project:
                raise serializers.ValidationError({"lines": "You can only use materials assigned to your project."})

        # ✅ Validate warehouse belongs to user's project
        if "warehouse" in data and data["warehouse"] is not None:
            if data["warehouse"] not in user.project.warehouses.all():
                raise serializers.ValidationError({"warehouse": "You can only use warehouses assigned to your project."})

        # ✅ Validate carrier belongs to user's project
        if "carrier" in data and data["carrier"] is not None:
            if data["carrier"] not in user.project.carriers.all():
                raise serializers.ValidationError({"carrier": "You can only use carriers assigned to your project."})

        # ✅ Ensure at least one order line is provided
        if not data.get('lines') or len(data.get('lines')) == 0:
            logger.warning("Validation failed: No order lines provided.")
            raise serializers.ValidationError({"lines": "At least one order line is required."})

        return data

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for line_data in lines_data:
                OrderLine.objects.create(order=order, **line_data)
            logger.info(f"Order created successfully: {order.lookup_code_order} with {len(lines_data)} lines.")
        return order