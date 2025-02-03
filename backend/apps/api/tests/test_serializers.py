from apps.api.serializers import OrderSerializer
from django.test import TestCase
from apps.orders.models import Order, OrderLine, Status, OrderType, OrderClass
from apps.inventory.models import Material, MaterialType, UOM
from apps.customers.models import Project, Customer
from apps.logistics.models import Warehouse, Contact, Address  # ✅ Importar Address
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from apps.inventory.models import Inventory

User = get_user_model()  # ✅ Obtener el modelo de usuario personalizado

class OrderSerializerTest(TestCase):
    def setUp(self):
        # ✅ Crear un usuario con un proyecto asignado
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User"
        )

        # ✅ Inicializar APIRequestFactory y simular una solicitud autenticada
        self.factory = APIRequestFactory()
        wsgi_request = self.factory.get("/")  # ✅ Crear una WSGIRequest normal
        force_authenticate(wsgi_request, user=self.user)  # ✅ Autenticar el usuario en la request

        # ✅ Convertirla en una Request de DRF (esto agrega `user`)
        self.request = Request(wsgi_request)
        
        # ✅ Crear estados válidos
        self.status_global = Status.objects.create(name="Active", status_type="Global")
        self.status_project = Status.objects.create(name="Project Active", status_type="Project")
        self.status_material = Status.objects.create(name="Material Active", status_type="Inventory")

        # ✅ Crear un cliente antes de crear el proyecto
        self.customer = Customer.objects.create(
            name="Test Customer",
            lookup_code="CUST001",
            status=self.status_global
        )

        # ✅ Crear un proyecto con un cliente y estado asignado
        self.project = Project.objects.create(
            name="Test Project",
            lookup_code="PRJ001",
            orders_prefix="TP",
            customer=self.customer,
            status=self.status_project
        )

        # ✅ Asignar un proyecto al usuario (IMPORTANTE)
        self.user.project = self.project
        self.user.save()

        # ✅ Crear un tipo de material válido
        self.material_type = MaterialType.objects.create(name="General", lookup_code="GEN")

        # ✅ Crear una unidad de medida válida
        self.uom = UOM.objects.create(name="Kilogram", lookup_code="KG")

        # ✅ Crear un material con un tipo, un proyecto, una unidad de medida y un estado asignado
        self.material = Material.objects.create(
            name="Test Material",
            lookup_code="MAT123",
            type=self.material_type,
            project=self.project,
            status=self.status_material,
            uom=self.uom
        )

        # ✅ Crear objetos para order_type, order_class, warehouse, contact, addresses
        self.order_type = OrderType.objects.create(type_name="Standard")
        self.order_class = OrderClass.objects.create(class_name="Regular")

        # ✅ Crear una dirección antes de crear el Warehouse
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
            address=self.warehouse_address,  # ✅ Asigna una dirección válida
            status=self.status_global
        )

        self.warehouse.projects.add(self.project)
        self.warehouse.save()

        Inventory.objects.create(
            project=self.project,
            material=self.material,
            warehouse=self.warehouse,
            quantity=10.0
        )

        self.contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone="123456789"
        )

        self.contact.projects.add(self.project)
        self.contact.save()

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

        # ✅ Modificar los valores en `self.valid_data` para usar los IDs correctos
        self.valid_data = {
            "lookup_code_order": "TEST0001",
            "lookup_code_shipment": "SHIP0001",
            "status": self.status_project.id,
            "order_type": self.order_type.id,
            "order_class": self.order_class.id,
            "project": self.project.id,
            "warehouse": self.warehouse.id,  # ✅ Ahora usa el ID correcto
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
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})  
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)
        self.assertTrue(is_valid)

    def test_invalid_project_restriction(self):
        self.valid_data["project"] = 999  # ID no válido
        serializer = OrderSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("project", serializer.errors)

    def test_insufficient_inventory(self):
        self.valid_data["lines"][0]["quantity"] = "100.00"  # Más de lo disponible
        serializer = OrderSerializer(data=self.valid_data, context={"request": self.request})  # ✅ Pasar contexto con request autenticada
        self.assertFalse(serializer.is_valid())
        self.assertIn("lines", serializer.errors)
