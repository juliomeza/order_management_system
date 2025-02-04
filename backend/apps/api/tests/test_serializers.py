from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from uuid import uuid4
from apps.api.serializers import OrderSerializer 
from apps.logistics.models import Carrier, CarrierService, Warehouse
from apps.inventory.models import Inventory
from apps.api.tests.test_base import BaseAPITestCase

class OrderSerializerTest(BaseAPITestCase):
    def setUp(self):
        """Set up test data"""
        super().setUp()
        
        # Create factory for request context
        self.factory = APIRequestFactory()
        wsgi_request = self.factory.get("/")
        self.request = Request(wsgi_request)
        self.request.user = self.user

        # Create carrier and carrier_service
        self.carrier = Carrier.objects.create(
            name="Test Carrier",
            lookup_code="CARR001"
        )
        self.carrier.projects.add(self.project)

        self.carrier_service = CarrierService.objects.create(
            name="Express",
            lookup_code="EXP",
            carrier=self.carrier
        )
        self.project.services.add(self.carrier_service)

        self.valid_data = {
            "lookup_code_order": "TEST0001",
            "lookup_code_shipment": "SHIP0001",
            "status": self.status_project.id,
            "order_type": self.order_type.id,
            "order_class": self.order_class.id,
            "project": self.project.id,
            "warehouse": self.warehouse.id,
            "contact": self.contact.id,
            "shipping_address": self.shipping_address.id,
            "billing_address": self.billing_address.id,
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
        """Test creating an order with valid data"""
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)
        self.assertTrue(is_valid)
        order = serializer.save()
        self.assertEqual(order.lines.count(), 1)

    def test_invalid_project_restriction(self):
        """Test creating an order with invalid project"""
        self.valid_data["project"] = self.other_project.id
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("project", serializer.errors)

    def test_insufficient_inventory(self):
        """Test creating an order with insufficient inventory"""
        self.valid_data["lines"][0]["quantity"] = "100.00"
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("lines", serializer.errors)

    def test_invalid_warehouse(self):
        """Test creating an order with warehouse not assigned to project"""
        new_warehouse = Warehouse.objects.create(
            name="Other Warehouse",
            lookup_code="WH002",
            address=self.warehouse_address,
            status=self.status_global
        )
        self.valid_data["warehouse"] = new_warehouse.id
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("warehouse", serializer.errors)

    def test_invalid_contact(self):
        """Test creating an order with contact not assigned to project"""
        other_contact = self.contact.__class__.objects.create(
            first_name="Other",
            last_name="Contact",
            phone="987654321"
        )
        self.valid_data["contact"] = other_contact.id
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("contact", serializer.errors)

    def test_valid_carrier_and_service(self):
        """Test creating an order with valid carrier and carrier service"""
        self.valid_data["carrier"] = self.carrier.id
        self.valid_data["service_type"] = self.carrier_service.id
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())

    def test_invalid_service_type(self):
        """Test creating an order with service type not belonging to carrier"""
        other_carrier = Carrier.objects.create(
            name="Other Carrier",
            lookup_code="CARR002"
        )
        other_service = CarrierService.objects.create(
            name="Other Service",
            lookup_code="OTH",
            carrier=other_carrier
        )
        self.valid_data["carrier"] = self.carrier.id
        self.valid_data["service_type"] = other_service.id
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("service_type", serializer.errors)

    def test_missing_lines(self):
        """Test creating an order without order lines"""
        self.valid_data["lines"] = []
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("lines", serializer.errors)

    def test_multiple_lines(self):
        """Test creating an order with multiple valid lines"""
        second_material = self.material.__class__.objects.create(
            name="Second Material",
            lookup_code="MAT456",
            type=self.material_type,
            project=self.project,
            status=self.status_material,
            uom=self.uom
        )
        
        # Create second inventory
        Inventory.objects.create(
            project=self.project,
            material=second_material,
            warehouse=self.warehouse,
            quantity=5.0,
            license_plate_id=f"LP{uuid4().hex[:8].upper()}"
        )

        self.valid_data["lines"].append({
            "material": second_material.id,
            "quantity": "3.00",
            "license_plate": None,
            "serial_number": None,
            "lot": "",
            "vendor_lot": "",
            "notes": ""
        })

        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.lines.count(), 2)