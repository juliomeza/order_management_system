from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.core.models import Status
from apps.customers.models import Project, Customer
from apps.logistics.models import Contact, Address, Warehouse
from apps.inventory.models import Material, MaterialType, UOM, Inventory
from apps.orders.models import OrderType, OrderClass
from uuid import uuid4

User = get_user_model()

class BaseAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for all test methods - used for data that can be shared between tests"""
        # Create statuses
        cls.status_global = Status.objects.create(
            name="Test Active",
            code="TEST_ACTIVE",
            status_type="Global",
            is_active=True
        )
        cls.status_project = Status.objects.create(
            name="Test Project",
            code="TEST_PROJECT",
            status_type="Global",
            is_active=True
        )
        cls.status_material = Status.objects.create(
            name="Test Material",
            code="TEST_MATERIAL",
            status_type="Global",
            is_active=True
        )

        # Create customer
        cls.customer = Customer.objects.create(
            name="Test Customer",
            lookup_code="CUST001",
            status=cls.status_global
        )

        # Create project
        cls.project = Project.objects.create(
            name="Test Project",
            lookup_code="PRJ001",
            orders_prefix="TP",
            customer=cls.customer,
            status=cls.status_project
        )

        # Create secondary customer and project for testing restrictions
        cls.other_customer = Customer.objects.create(
            name="Other Customer",
            lookup_code="CUST002",
            status=cls.status_global
        )
        
        cls.other_project = Project.objects.create(
            name="Other Project",
            lookup_code="PRJ002",
            orders_prefix="OP",
            customer=cls.other_customer,
            status=cls.status_project
        )

    def setUp(self):
        """Set up data for each test method"""
        # Create user and assign project
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            status=self.status_global,
            project=self.project
        )

        # Setup authentication
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

        # Create base objects that might be modified in tests
        self._create_inventory_objects()
        self._create_logistics_objects()
        self._create_order_objects()

    def _create_inventory_objects(self):
        """Create inventory-related objects"""
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

    def _create_logistics_objects(self):
        """Create logistics-related objects"""
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

        # Create inventory with unique license plate
        self.inventory = Inventory.objects.create(
            project=self.project,
            material=self.material,
            warehouse=self.warehouse,
            quantity=10.0,
            license_plate_id=f"LP{uuid4().hex[:8].upper()}"
        )

    def _create_order_objects(self):
        """Create order-related objects"""
        self.order_type = OrderType.objects.create(type_name="Standard")
        self.order_class = OrderClass.objects.create(class_name="Regular")