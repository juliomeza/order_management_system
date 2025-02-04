from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.orders.models import Order, OrderType, OrderClass, Project
from apps.core.models import Status
from apps.customers.models import Customer
from apps.inventory.models import Material, MaterialType, UOM, Inventory
from apps.logistics.models import Warehouse, Contact, Address

User = get_user_model()

class OrderAPITestCase(APITestCase):
    def setUp(self):
        # Create statuses
        self.status_global = Status.objects.create(
            name="Active",
            status_type="Global",
            is_active=True
        )
        self.status_project = Status.objects.create(
            name="Project Active",
            status_type="Project",
            is_active=True
        )
        self.status_material = Status.objects.create(
            name="Material Active",
            status_type="Inventory",
            is_active=True
        )

        # Create customer
        self.customer = Customer.objects.create(
            name="Test Customer",
            lookup_code="CUST001",
            status=self.status_global
        )

        # Create project
        self.project = Project.objects.create(
            name="Test Project",
            lookup_code="PRJ001",
            orders_prefix="TP",
            customer=self.customer,
            status=self.status_project
        )

        # Create user and assign project
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )
        self.user.project = self.project
        self.user.save()

        # Setup authentication
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create material type and UOM
        self.material_type = MaterialType.objects.create(
            name="General",
            lookup_code="GEN"
        )
        self.uom = UOM.objects.create(
            name="Kilogram",
            lookup_code="KG"
        )

        # Create material
        self.material = Material.objects.create(
            name="Test Material",
            lookup_code="MAT123",
            type=self.material_type,
            project=self.project,
            status=self.status_material,
            uom=self.uom
        )

        # Create warehouse with address
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

        # Create inventory
        self.inventory = Inventory.objects.create(
            project=self.project,
            material=self.material,
            warehouse=self.warehouse,
            quantity=10.0
        )

        # Create contact
        self.contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone="123456789"
        )
        self.contact.projects.add(self.project)

        # Create addresses
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

        # Create order type and class
        self.order_type = OrderType.objects.create(type_name="Standard")
        self.order_class = OrderClass.objects.create(class_name="Regular")

        # Valid payload for creating orders
        self.valid_payload = {
            "lookup_code_order": "TEST123",
            "lookup_code_shipment": "SHIP123",
            "project": self.project.id,
            "status": self.status_project.id,
            "order_type": self.order_type.id,
            "order_class": self.order_class.id,
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

    def test_get_orders_success(self):
        """Test retrieving orders for authenticated user"""
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_unauthorized(self):
        """Test retrieving orders without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_success(self):
        """Test creating a valid order"""
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().lookup_code_order, "TEST123")

    def test_create_order_unauthorized(self):
        """Test creating order without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_invalid_project(self):
        """Test creating order for invalid project"""
        # Create another project
        other_project = Project.objects.create(
            name="Other Project",
            lookup_code="PRJ002",
            orders_prefix="OP",
            customer=self.customer,
            status=self.status_project
        )
        
        self.valid_payload["project"] = other_project.id
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_insufficient_inventory(self):
        """Test creating order with insufficient inventory"""
        self.valid_payload["lines"][0]["quantity"] = "100.00"  # More than available
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_missing_lines(self):
        """Test creating order without order lines"""
        self.valid_payload["lines"] = []
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)