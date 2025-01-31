from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from apps.core.models import Status, Role, TimeStampedModel
from apps.logistics.models import Warehouse, Carrier, CarrierService
from apps.core.validators import validate_lookup_code, StatusValidator

class Customer(TimeStampedModel):
   """
   Root entity for multi-tenant structure
   """
   OUTPUT_FORMAT_CHOICES = [
       ('CSV', 'CSV'),
       ('JSON', 'JSON'),
   ]

   name = models.CharField(max_length=100)
   lookup_code = models.CharField(
       max_length=50,
       unique=True,
       validators=[validate_lookup_code]
   )
   status = models.ForeignKey(
       Status,
       on_delete=models.PROTECT,
       related_name='customers'
   )
   address = models.ForeignKey(
       'logistics.Address',
       on_delete=models.PROTECT,
       related_name='customers',
       null=True
   )
   output_format = models.CharField(
       max_length=4,
       choices=OUTPUT_FORMAT_CHOICES,
       default='JSON'
   )
   notes = models.TextField(blank=True)

   def clean(self):
        """
        Custom validation logic applied before saving.
        """
        validator = StatusValidator('Global')
        validator(self.status)

   def __str__(self):
       return f"{self.name}"

class Project(TimeStampedModel):
   """
   Organize customer operations
   """
   name = models.CharField(max_length=100)
   lookup_code = models.CharField(
       max_length=50,
       unique=True,
       validators=[validate_lookup_code]
   )
   orders_prefix = models.CharField(
       max_length=10,
       unique=True,
       validators=[MinLengthValidator(2)],
       help_text="Unique prefix for order numbers"
   )
   status = models.ForeignKey(
       Status,
       on_delete=models.PROTECT,
       related_name='projects'
   )
   customer = models.ForeignKey(
       Customer,
       on_delete=models.PROTECT,
       related_name='projects'
   )
   warehouses = models.ManyToManyField(
       'logistics.Warehouse',
       related_name='projects',
       blank=True
   )
   carriers = models.ManyToManyField(
       'logistics.Carrier',
       related_name='projects', 
       blank=True
   )
   services = models.ManyToManyField(
       'logistics.CarrierService',
       related_name='projects',
       blank=True
   )
   contacts = models.ManyToManyField(
       'logistics.Contact',
       related_name='projects',
       blank=True
   )
   notes = models.TextField(blank=True)

   def clean(self):
        """
        Custom validation logic applied before saving.
        """
        validator = StatusValidator('Global')
        validator(self.status)

   class Meta:
       indexes = [
           models.Index(fields=['customer', 'status']),
       ]

   def __str__(self):
       return f"{self.name}"

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='users',
        null=True,
        default=lambda: Status.objects.get(name="Active")
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='users',
        null=True,
        blank=True
    )
    role = models.ForeignKey(
        'core.Role',
        on_delete=models.PROTECT,
        related_name='users',
        null=True
    )

    # Fields required for extending AbstractUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def clean(self):
        """
        Custom validation logic applied before saving.
        """
        validator = StatusValidator('Global')
        validator(self.status)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'username']),
            models.Index(fields=['project', 'role']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name