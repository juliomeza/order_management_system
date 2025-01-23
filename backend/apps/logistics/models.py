from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from apps.core.models import TimeStampedModel, Status

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
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    
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
        return f"{self.address_line_1}, {self.city}, {self.state}"

class Contact(TimeStampedModel):
    """
    Contact information management
    """
    CONTACT_TYPES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=100, blank=True)
    contact_type = models.CharField(
        max_length=10,
        choices=CONTACT_TYPES,
        default='primary'
    )
    addresses = models.ManyToManyField(
        'Address',
        through='ContactAddress',
        related_name='contact_addresses'
    )
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ContactAddress(TimeStampedModel):
    """
    Manages the relationship between Contact and Address
    """
    contact = models.ForeignKey('Contact', on_delete=models.PROTECT)
    address = models.ForeignKey('Address', on_delete=models.PROTECT)
    is_primary = models.BooleanField(default=False)
    address_type = models.CharField(
        max_length=10,
        choices=Address.ADDRESS_TYPES,
        default='shipping'
    )

    class Meta:
        unique_together = [['contact', 'address', 'address_type']]
        indexes = [
            models.Index(fields=['contact', 'is_primary']),
            models.Index(fields=['address', 'address_type']),
        ]

    def __str__(self):
        return f"{self.contact} - {self.address} ({self.address_type})"

class Warehouse(TimeStampedModel):
    """
    Physical location management
    """
    name = models.CharField(max_length=100)
    lookup_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='warehouses'
    )
    notes = models.TextField(blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='warehouses'
    )

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
        validators=[MinLengthValidator(2)]
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
        validators=[MinLengthValidator(2)]
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