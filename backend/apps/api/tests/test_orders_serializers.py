from uuid import uuid4
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from apps.api.serializers import OrderSerializer
from rest_framework.test import APITestCase
from apps.api.tests.factories import (
    StatusFactory, ProjectFactory, UserFactory, MaterialFactory, 
    WarehouseFactory, ContactFactory, AddressFactory, OrderTypeFactory,
    OrderClassFactory, CarrierFactory, CarrierServiceFactory, InventoryFactory
)

class OrderSerializerTest(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create factory for request context
        self.factory = APIRequestFactory()
        wsgi_request = self.factory.get("/")
        self.request = Request(wsgi_request)

        # Create base objects
        self.status = StatusFactory()
        self.project = ProjectFactory()
        self.user = UserFactory(project=self.project)
        self.request.user = self.user

        # Create order-related objects
        self.order_type = OrderTypeFactory()
        self.order_class = OrderClassFactory()
        self.warehouse = WarehouseFactory()
        self.warehouse.projects.add(self.project)
        
        self.contact = ContactFactory()
        self.contact.projects.add(self.project)
        
        self.shipping_address = AddressFactory(
            entity_type='recipient',
            address_type='shipping'
        )
        self.billing_address = AddressFactory(
            entity_type='recipient',
            address_type='billing'
        )

        # Create material and inventory
        self.material = MaterialFactory(project=self.project)
        self.inventory = InventoryFactory(
            project=self.project,
            material=self.material,
            warehouse=self.warehouse,
            quantity=10.0
        )

        # Create carrier and service
        self.carrier = CarrierFactory()
        self.carrier.projects.add(self.project)
        
        self.carrier_service = CarrierServiceFactory(carrier=self.carrier)
        self.project.services.add(self.carrier_service)

        self.valid_data = {
            "lookup_code_order": "TEST0001",
            "lookup_code_shipment": "SHIP0001",
            "status": self.status.id,
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
        other_project = ProjectFactory()
        self.valid_data["project"] = other_project.id
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
        new_warehouse = WarehouseFactory()  # Not assigned to project
        self.valid_data["warehouse"] = new_warehouse.id
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("warehouse", serializer.errors)

    def test_invalid_contact(self):
        """Test creating an order with contact not assigned to project"""
        other_contact = ContactFactory()  # Not assigned to project
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
        other_carrier = CarrierFactory()
        other_service = CarrierServiceFactory(carrier=other_carrier)
        
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
        second_material = MaterialFactory(project=self.project)
        InventoryFactory(
            project=self.project,
            material=second_material,
            warehouse=self.warehouse,
            quantity=5.0
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