from django.test import TestCase
from apps.orders.models import Order, OrderLine, Status
from apps.inventory.models import Material
from apps.api.serializers import OrderSerializer

class OrderSerializerTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Pending", status_type="Orders")
        self.material = Material.objects.create(name="Test Material", lookup_code="MAT123")

        self.valid_data = {
            "lookup_code_order": "TEST0001",
            "lookup_code_shipment": "SHIP0001",
            "status": self.status.id,
            "order_type": 1,
            "order_class": 1,
            "project": 1,
            "warehouse": 1,
            "contact": 1,
            "shipping_address": 1,
            "billing_address": 1,
            "carrier": None,
            "service_type": None,
            "expected_delivery_date": "2025-02-05T14:15:51Z",
            "notes": "",
            "lines": [
                {
                    "material": self.material.id,
                    "quantity": "2.00",
                    "license_plate": None,
                    "serial_number": None,
                    "lot": "",
                    "vendor_lot": "",
                    "notes": ""
                }
            ]
        }

    def test_valid_order_serializer(self):
        serializer = OrderSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_project_restriction(self):
        self.valid_data["project"] = 999  # ID no válido
        serializer = OrderSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("project", serializer.errors)

    def test_insufficient_inventory(self):
        self.valid_data["lines"][0]["quantity"] = "100.00"  # Más de lo disponible
        serializer = OrderSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("lines", serializer.errors)
