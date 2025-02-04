import factory
from uuid import uuid4
from django.contrib.auth import get_user_model
from apps.core.models import Status
from apps.customers.models import Project, Customer
from apps.logistics.models import Contact, Address, Carrier, CarrierService, Warehouse
from apps.inventory.models import Material, MaterialType, UOM, Inventory
from apps.orders.models import Order, OrderType, OrderClass, OrderLine

class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
    
    name = factory.Sequence(lambda n: f"Test Active {n}")
    code = factory.Sequence(lambda n: f"TEST_ACTIVE_{n}")
    status_type = "Global"
    is_active = True

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer
    
    name = factory.Sequence(lambda n: f"Test Customer {n}")
    lookup_code = factory.Sequence(lambda n: f"CUST{n}")
    status = factory.SubFactory(StatusFactory)

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project
    
    name = factory.Sequence(lambda n: f"Test Project {n}")
    lookup_code = factory.Sequence(lambda n: f"PRJ{n}")
    orders_prefix = factory.Sequence(lambda n: f"TP{n}")  # Haciendo único el prefix
    status = factory.SubFactory(StatusFactory)
    customer = factory.SubFactory(CustomerFactory)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'testpass')
    status = factory.SubFactory(StatusFactory)
    project = factory.SubFactory(ProjectFactory)
    is_active = True

class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    address_line_1 = factory.Sequence(lambda n: f"123 Test Street {n}")
    address_line_2 = factory.Sequence(lambda n: f"Suite {n}")
    city = "Miami"
    state = "FL"
    postal_code = factory.Sequence(lambda n: f"33{str(n).zfill(3)}")
    country = "USA"
    entity_type = "recipient"
    address_type = "shipping"
    notes = factory.Sequence(lambda n: f"Test address {n}")

class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    first_name = factory.Sequence(lambda n: f"John{n}")
    last_name = factory.Sequence(lambda n: f"Doe{n}")
    phone = factory.Sequence(lambda n: f"123456789{n}")
    email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@example.com".lower())
    mobile = factory.Sequence(lambda n: f"987654321{n}")
    title = factory.Sequence(lambda n: f"Manager {n}")
    notes = factory.Sequence(lambda n: f"Test contact {n}")

    @factory.post_generation
    def projects(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.projects.add(*extracted)

    @factory.post_generation
    def addresses(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for address_type in extracted:
                AddressFactory(
                    entity_type='recipient',
                    address_type=address_type,
                    contact=self
                )

class MaterialTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MaterialType

    name = factory.Sequence(lambda n: f"Material Type {n}")
    lookup_code = factory.Sequence(lambda n: f"MT{n}")

class UOMFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UOM

    name = factory.Sequence(lambda n: f"UOM {n}")
    lookup_code = factory.Sequence(lambda n: f"UOM{n}")

class MaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Material

    name = factory.Sequence(lambda n: f"Material {n}")
    lookup_code = factory.Sequence(lambda n: f"MAT{n}")
    type = factory.SubFactory(MaterialTypeFactory)
    project = factory.SubFactory(ProjectFactory)
    status = factory.SubFactory(StatusFactory)
    uom = factory.SubFactory(UOMFactory)

class WarehouseAddressFactory(AddressFactory):
    entity_type = "warehouse"
    address_type = "shipping"

class WarehouseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Warehouse

    name = factory.Sequence(lambda n: f"Warehouse {n}")
    lookup_code = factory.Sequence(lambda n: f"WH{n}")
    address = factory.SubFactory(WarehouseAddressFactory)
    status = factory.SubFactory(StatusFactory)

    @factory.post_generation
    def projects(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.projects.add(*extracted)

class InventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventory

    project = factory.SubFactory(ProjectFactory)
    material = factory.SubFactory(MaterialFactory)
    warehouse = factory.SubFactory(WarehouseFactory)
    quantity = factory.Sequence(lambda n: float(n + 10))
    license_plate_id = factory.LazyFunction(lambda: f"LP{uuid4().hex[:8].upper()}")

class OrderTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderType

    type_name = factory.Sequence(lambda n: f"Order Type {n}")

class OrderClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderClass

    class_name = factory.Sequence(lambda n: f"Order Class {n}")

class CarrierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Carrier

    name = factory.Sequence(lambda n: f"Carrier {n}")
    lookup_code = factory.Sequence(lambda n: f"CARR{n}")

    @factory.post_generation
    def projects(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.projects.add(*extracted)

class CarrierServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarrierService

    name = factory.Sequence(lambda n: f"Service {n}")
    lookup_code = factory.Sequence(lambda n: f"SVC{n}")
    carrier = factory.SubFactory(CarrierFactory)

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    lookup_code_order = factory.Sequence(lambda n: f"ORD{n}")
    lookup_code_shipment = factory.Sequence(lambda n: f"SHIP{n}")
    project = factory.SubFactory(ProjectFactory)
    status = factory.SubFactory(StatusFactory)
    order_type = factory.SubFactory(OrderTypeFactory)
    order_class = factory.SubFactory(OrderClassFactory)
    warehouse = factory.SubFactory(WarehouseFactory)
    contact = factory.SubFactory(ContactFactory)
    shipping_address = factory.SubFactory(AddressFactory)
    billing_address = factory.SubFactory(AddressFactory)
    carrier = None
    service_type = None
    expected_delivery_date = factory.Faker('future_datetime')