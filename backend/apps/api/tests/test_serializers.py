from apps.api.serializers import OrderSerializer
from django.test import TestCase
from apps.orders.models import Order, OrderLine, Status, OrderType, OrderClass
from apps.inventory.models import Material, MaterialType, UOM, Inventory
from apps.customers.models import Project, Customer
from apps.logistics.models import Warehouse, Contact, Address, Carrier, CarrierService
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from uuid import uuid4

User = get_user_model()

class OrderSerializerTest(TestCase):
    def setUp(self):
        # Base setup (mantener el existente)
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User"
        )

        self.factory = APIRequestFactory()
        wsgi_request = self.factory.get("/")
        force_authenticate(wsgi_request, user=self.user)
        self.request = Request(wsgi_request)
        
        self.status_global = Status.objects.create(name="Active", status_type="Global")
        self.status_project = Status.objects.create(name="Project Active", status_type="Project")
        self.status_material = Status.objects.create(name="Material Active", status_type="Inventory")

        self.customer = Customer.objects.create(
            name="Test Customer",
            lookup_code="CUST001",
            status=self.status_global
        )

        self.project = Project.objects.create(
            name="Test Project",
            lookup_code="PRJ001",
            orders_prefix="TP",
            customer=self.customer,
            status=self.status_project
        )

        self.user.project = self.project
        self.user.save()

        self.material_type = MaterialType.objects.create(name="General", lookup_code="GEN")
        self.uom = UOM.objects.create(name="Kilogram", lookup_code="KG")

        self.material = Material.objects.create(
            name="Test Material",
            lookup_code="MAT123",
            type=self.material_type,
            project=self.project,
            status=self.status_material,
            uom=self.uom
        )

        self.order_type = OrderType.objects.create(type_name="Standard")
        self.order_class = OrderClass.objects.create(class_name="Regular")

        self.warehouse_address = Address.objects.create(
            address_line_1="789 Warehouse Rd",
            city="Miami",
            state="FL",
            postal_code="33103",
            country="USA",
            entity_type="warehouse",
            address_type="shipping"
        )

        self.warehouse = Warehouse.objects.create(
            name="Main Warehouse",
            lookup_code="WH001",
            address=self.warehouse_address,
            status=self.status_global
        )
        self.warehouse.projects.add(self.project)

        # Crear carrier y carrier_service
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

        # Crear inventario con license_plate_id único
        Inventory.objects.create(
            project=self.project,
            material=self.material,
            warehouse=self.warehouse,
            quantity=10.0,
            license_plate_id=f"LP{uuid4().hex[:8].upper()}"
        )

        self.contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone="123456789"
        )
        self.contact.projects.add(self.project)

        self.shipping_address = Address.objects.create(
            address_line_1="123 Shipping St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="USA",
            entity_type="customer",
            address_type="shipping"
        )

        self.billing_address = Address.objects.create(
            address_line_1="456 Billing Ave",
            city="Miami",
            state="FL",
            postal_code="33102",
            country="USA",
            entity_type="customer",
            address_type="billing"
        )

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
        other_project = Project.objects.create(
            name="Other Project",
            customer=Customer.objects.create(
                name="Other Customer",
                lookup_code="CUST002",
                status=self.status_global
            ),
            status=self.status_project
        )
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
        other_warehouse = Warehouse.objects.create(
            name="Other Warehouse",
            lookup_code="WH002",
            address=Address.objects.create(
                address_line_1="Other Address",
                city="Other City",
                state="FL",
                postal_code="33333",
                country="USA",
                entity_type="warehouse"
            ),
            status=self.status_global
        )
        self.valid_data["warehouse"] = other_warehouse.id
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("warehouse", serializer.errors)

    def test_invalid_contact(self):
        """Test creating an order with contact not assigned to project"""
        other_contact = Contact.objects.create(
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
        second_material = Material.objects.create(
            name="Second Material",
            lookup_code="MAT456",
            type=self.material_type,
            project=self.project,
            status=self.status_material,
            uom=self.uom
        )
        
        # Crear segundo inventario con license_plate_id único
        Inventory.objects.create(
            project=self.project,
            material=second_material,
            warehouse=self.warehouse,
            quantity=5.0,
            license_plate_id=f"LP{uuid4().hex[:8].upper()}"  # Genera un ID único
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