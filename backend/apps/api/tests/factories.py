import factory
from django.contrib.auth import get_user_model
from apps.core.models import Status
from apps.customers.models import Project, Customer

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