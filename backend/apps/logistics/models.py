from django.db import models
from django.core.validators import MinLengthValidator
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
    
    # Entity reference (polymorphic)
    entity_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of customer/warehouse"
    )
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
    attention_of = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Addresses"
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['country', 'state', 'city']),
        ]

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state}"

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
        return f"{self.name} ({self.lookup_code})"

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
        return f"{self.name} ({self.lookup_code})"

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