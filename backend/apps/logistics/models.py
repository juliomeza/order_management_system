from django.db import models
from django.core.validators import EmailValidator
from apps.core.models import TimeStampedModel, Status
from apps.core.validators import validate_lookup_code, StatusValidator

class Address(TimeStampedModel):
    """
    Standardized address management
    """
    ADDRESS_TYPES = [
        ('shipping', 'Shipping'),
        ('billing', 'Billing'),
    ]

    ENTITY_TYPES = [
        ('customer', 'Customer'),
        ('warehouse', 'Warehouse'),
        ('recipient', 'Recipient'),
    ]

    # Address fields
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    
    entity_type = models.CharField(
        max_length=20,
        choices=ENTITY_TYPES
    )
    
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPES,
        default='shipping'
    )
    
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Addresses"
        indexes = [
            models.Index(fields=['entity_type']),
            models.Index(fields=['country', 'state', 'city']),
        ]

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state} {self.postal_code}"

class Contact(TimeStampedModel):
    """
    Contact information management
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(validators=[EmailValidator()], blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=100, blank=True)
    addresses = models.ManyToManyField(
       'Address',
       related_name='contacts',
       blank=True
   )
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Warehouse(TimeStampedModel):
    """
    Physical location management
    """
    name = models.CharField(max_length=100)
    lookup_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_lookup_code]
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='warehouses'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='warehouses'
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
            models.Index(fields=['lookup_code']),
        ]

    def __str__(self):
        return f"{self.name}"

class Carrier(TimeStampedModel):
    """
    Shipping provider management
    """
    name = models.CharField(max_length=100)
    lookup_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_lookup_code]
    )

    class Meta:
        indexes = [
            models.Index(fields=['lookup_code']),
        ]

    def __str__(self):
        return f"{self.name}"

class CarrierService(TimeStampedModel):
    """
    Specific shipping service options
    """
    name = models.CharField(max_length=100)
    lookup_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_lookup_code]
    )
    carrier = models.ForeignKey(
        Carrier,
        on_delete=models.PROTECT,
        related_name='services'
    )

    class Meta:
        indexes = [
            models.Index(fields=['lookup_code']),
            models.Index(fields=['carrier']),
        ]

    def __str__(self):
        return f"{self.carrier.name} - {self.name}"