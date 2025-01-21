from django.db import models
from django.core.validators import MinLengthValidator
from apps.core.models import TimeStampedModel, Status
from apps.customers.models import Project

class OrderClass(TimeStampedModel):
    """
    Categorize orders by type and processing rules
    """
    className = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Order Classes"

    def __str__(self):
        return self.className

class Order(TimeStampedModel):
    """
    Core business transaction record
    """
    ORDER_TYPES = [
        ('INBOUND', 'Inbound'),
        ('OUTBOUND', 'Outbound'),
    ]

    # Lookup Codes
    lookupCodeOrder = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text="Unique order identifier"
    )
    lookupCodeShipment = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text="Unique shipment identifier"
    )

    # Status and Type
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    orderType = models.CharField(
        max_length=8,
        choices=ORDER_TYPES,
        help_text="INBOUND: Receiving inventory, OUTBOUND: Shipping to customers"
    )

    # Foreign Keys
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    warehouse = models.ForeignKey(
        'logistics.Warehouse',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    carrier = models.ForeignKey(
        'logistics.Carrier',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    serviceType = models.ForeignKey(
        'logistics.CarrierService',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    address = models.ForeignKey(
        'logistics.Address',
        on_delete=models.PROTECT,
        related_name='shipping_orders'
    )
    billingAddress = models.ForeignKey(
        'logistics.Address',
        on_delete=models.PROTECT,
        related_name='billing_orders'
    )
    orderClass = models.ForeignKey(
        OrderClass,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    # Additional Fields
    expectedDeliveryDate = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['lookupCodeOrder']),
            models.Index(fields=['lookupCodeShipment']),
            models.Index(fields=['expectedDeliveryDate']),
        ]

    def __str__(self):
        return f"{self.orderType} - {self.lookupCodeOrder}"

    def save(self, *args, **kwargs):
        # Here you could add logic to validate order numbers based on project prefix
        super().save(*args, **kwargs)