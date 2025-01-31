from rest_framework import serializers
from apps.orders.models import Order, OrderLine
from apps.logistics.models import Contact, Address
import logging
from django.db import transaction

logger = logging.getLogger('custom_logger')

# Create a new order with order lines
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
        
        # ✅ Validate service_type belongs to the selected carrier
        if "service_type" in data and data["service_type"] is not None:
            if data["service_type"] not in data["carrier"].services.all():
                raise serializers.ValidationError({"service_type": "This service type is not available for the selected carrier."})

            # ✅ Validate service_type belongs to the user's project (NEW)
            if data["service_type"] not in user.project.services.all():
                raise serializers.ValidationError({"service_type": "This service type is not assigned to your project."})

        # ✅ Validate contact belongs to user's project
        if "contact" in data and data["contact"] is not None:
            if data["contact"] not in user.project.contacts.all():
                raise serializers.ValidationError({"contact": "You can only select contacts assigned to your project."})

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

# Create new contact with addressess
class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and managing shipping and billing addresses.
    """

    entity_type = serializers.CharField(required=False)

    class Meta:
        model = Address
        fields = ['id', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country', 'address_type', 'entity_type', 'notes']

    def create(self, validated_data):
        """
        Assign the new address to the authenticated user's customer.
        """
        user = self.context['request'].user
        validated_data['entity_type'] = 'recipient'  # ✅ Ensure the address is linked to a customer
        address = Address.objects.create(**validated_data)
        return address

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and managing project contacts along with multiple addresses.
    """
    addresses = AddressSerializer(many=True, required=False)  # ✅ Allow multiple addresses in one request

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'mobile', 'title', 'addresses', 'notes']

    def create(self, validated_data):
        """
        Assign the new contact to the authenticated user's project and create associated addresses.
        """
        user = self.context['request'].user
        addresses_data = validated_data.pop('addresses', [])  # ✅ Extract addresses from request

        # ✅ Crear el contacto sin el project (porque es ManyToMany)
        contact = Contact.objects.create(**validated_data)

        # ✅ Asociar el contacto con el proyecto del usuario
        user.project.contacts.add(contact)  

        # ✅ Crear y asociar direcciones al contacto
        for address_data in addresses_data:
            address_data['entity_type'] = 'recipient'  # ✅ Ensure it's for a recipient
            address = Address.objects.create(**address_data)
            contact.addresses.add(address)  # ✅ Link address to contact

        return contact