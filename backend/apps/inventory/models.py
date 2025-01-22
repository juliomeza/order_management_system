from django.db import models
from django.core.validators import MinLengthValidator
from apps.core.models import TimeStampedModel, Status
from apps.customers.models import Project

class UOM(TimeStampedModel):
    """
    Units of Measure for materials
    """
    name = models.CharField(max_length=50)
    lookup_code = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    description = models.TextField(blank=True)

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
    lookup_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
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
    is_serialized = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    uom = models.ForeignKey(
        UOM,
        on_delete=models.PROTECT,
        related_name='materials'
    )

    class Meta:
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['lookup_code']),
        ]

    def __str__(self):
        return f"{self.name} ({self.lookup_code})"

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
    location = models.CharField(max_length=50)
    license_plate_id = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    license_plate = models.CharField(max_length=50)
    lot = models.CharField(max_length=50, blank=True)
    vendor_lot = models.CharField(max_length=50, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by_user = models.ForeignKey(
        'customers.User',
        on_delete=models.PROTECT,
        related_name='inventory_updates'
    )

    class Meta:
        verbose_name_plural = "Inventories"
        indexes = [
            models.Index(fields=['project', 'warehouse', 'material']),
            models.Index(fields=['license_plate_id']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.material.name} at {self.warehouse.name} ({self.quantity})"

class InventorySerialNumber(TimeStampedModel):
    """
    Track individual serialized units within inventory
    """
    lookup_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
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