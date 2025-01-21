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

    # Address fields
    addressLine1 = models.CharField(max_length=100)
    addressLine2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=20)
    
    # Entity reference (polymorphic)
    entityID = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of customer/warehouse"
    )
    entityType = models.CharField(
        max_length=20,
        choices=[
            ('customer', 'Customer'),
            ('warehouse', 'Warehouse'),
        ]
    )
    
    addressType = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPES,
        default='shipping'
    )
    
    notes = models.TextField(blank=True)
    attentionOf = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Addresses"
        indexes = [
            models.Index(fields=['entityType', 'entityID']),
            models.Index(fields=['country', 'state', 'city']),
        ]

    def __str__(self):
        return f"{self.addressLine1}, {self.city}, {self.state}"

class Warehouse(TimeStampedModel):
    """
    Physical location management
    """
    name = models.CharField(max_length=100)
    lookupCode = models.CharField(
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
            models.Index(fields=['lookupCode']),
        ]

    def __str__(self):
        return f"{self.name} ({self.lookupCode})"

class Carrier(TimeStampedModel):
    """
    Shipping provider management
    """
    name = models.CharField(max_length=100)
    lookupCode = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)]
    )

    class Meta:
        indexes = [
            models.Index(fields=['lookupCode']),
        ]

    def __str__(self):
        return f"{self.name} ({self.lookupCode})"

class CarrierService(TimeStampedModel):
    """
    Specific shipping service options
    """
    name = models.CharField(max_length=100)
    lookupCode = models.CharField(
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
            models.Index(fields=['lookupCode']),
            models.Index(fields=['carrier']),
        ]

    def __str__(self):
        return f"{self.carrier.name} - {self.name}"