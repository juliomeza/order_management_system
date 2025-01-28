from django.db import models
from django.core.validators import MinLengthValidator
from apps.core.models import TimeStampedModel, Status
from apps.customers.models import Project
from django.utils.timezone import now
from apps.core.validators import validate_lookup_code

class UOM(TimeStampedModel):
    """
    Units of Measure for materials
    """
    name = models.CharField(max_length=50)
    lookup_code = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_lookup_code]
    )
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Unit of Measure"
        verbose_name_plural = "Units of Measure"
        indexes = [
            models.Index(fields=['lookup_code']),
        ]

    def __str__(self):
        return f"{self.name} ({self.lookup_code})"

class Material(TimeStampedModel):
    """
    Product catalog management
    """
    name = models.CharField(max_length=100)
    lookup_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_lookup_code]
    )
    description = models.CharField(max_length=100, blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='materials'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='materials'
    )
    type = models.CharField(max_length=50)
    uom = models.ForeignKey(
        UOM,
        on_delete=models.PROTECT,
        related_name='materials'
    )
    is_serialized = models.BooleanField(default=False)

    def current_price(self):
        price_history = self.price_history.filter(
            effective_date__lte=now()
        ).order_by('-effective_date').first()
        return price_history.price if price_history else None
    current_price.short_description = 'Current Price'

    class Meta:
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['lookup_code']),
        ]

    def __str__(self):
        return f"{self.name}"

class MaterialPriceHistory(TimeStampedModel):
    """
    Price history for materials
    """
    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name='price_history'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['material', 'effective_date', 'end_date']),
        ]
    
    def __str__(self):
        return f"{self.material.name} - ${self.price} (from {self.effective_date.date()})"

class Inventory(TimeStampedModel):
    """
    Track material quantities and locations
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='inventories'
    )
    warehouse = models.ForeignKey(
        'logistics.Warehouse',
        on_delete=models.PROTECT,
        related_name='inventories'
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name='inventories'
    )
    location = models.CharField(max_length=50, blank=True)
    license_plate_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        validators=[MinLengthValidator(2)]
    )
    license_plate = models.CharField(max_length=50, blank=True)
    lot = models.CharField(max_length=50, blank=True)
    vendor_lot = models.CharField(max_length=50, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Inventories"
        indexes = [
            models.Index(fields=['project', 'warehouse', 'material']),
            models.Index(fields=['license_plate_id']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.license_plate} ({self.quantity})"

class InventorySerialNumber(TimeStampedModel):
    """
    Track individual serialized units within inventory
    """
    lookup_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_lookup_code],
        help_text="Serial number"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='serial_numbers'
    )
    license_plate = models.ForeignKey(
        Inventory,
        on_delete=models.PROTECT,
        related_name='serial_numbers'
    )
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['lookup_code']),
            models.Index(fields=['license_plate']),
        ]

    def __str__(self):
        return f"SN: {self.lookup_code}"