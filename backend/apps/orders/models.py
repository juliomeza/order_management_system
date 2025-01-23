from django.db import models
from django.core.validators import MinLengthValidator
from apps.core.models import TimeStampedModel, Status
from apps.customers.models import Project

class OrderClass(TimeStampedModel):
    """
    Categorize orders by type and processing rules
    """
    class_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Order Classes"

    def __str__(self):
        return self.class_name


class OrderType(TimeStampedModel):
    """
    Flexible type management for various entities
    """
    type_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Order Types"

    def __str__(self):
        return f"{self.type_name}"

class Order(TimeStampedModel):
    """
    Core business transaction record
    """
    ORDER_TYPES = [
        ('INBOUND', 'Inbound'),
        ('OUTBOUND', 'Outbound'),
    ]

    # Lookup Codes
    lookup_code_order = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text="Unique order identifier"
    )
    lookup_code_shipment = models.CharField(
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
    order_type = models.CharField(
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
        related_name='orders',
        null=True,
        blank=True
    )
    service_type = models.ForeignKey(
        'logistics.CarrierService',
        on_delete=models.PROTECT,
        related_name='orders',
        null=True,
        blank=True
    )
    contact = models.ForeignKey(
        'logistics.Contact',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    shipping_address = models.ForeignKey(
        'logistics.Address',
        on_delete=models.PROTECT,
        related_name='shipping_orders'
    )
    billing_address = models.ForeignKey(
        'logistics.Address',
        on_delete=models.PROTECT,
        related_name='billing_orders'
    )
    order_class = models.ForeignKey(
        OrderClass,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    # Additional Fields
    expected_delivery_date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['lookup_code_order']),
            models.Index(fields=['lookup_code_shipment']),
            models.Index(fields=['expected_delivery_date']),
        ]

    def __str__(self):
        return f"{self.order_type} - {self.lookup_code_order}"

    def save(self, *args, **kwargs):
        # Here you could add logic to validate order numbers based on project prefix
        super().save(*args, **kwargs)

class OrderLine(TimeStampedModel):
   """
   Track individual line items within orders
   """
   order = models.ForeignKey(
       'Order',
       on_delete=models.PROTECT,
       related_name='lines'
   )
   material = models.ForeignKey(
       'inventory.Material',
       on_delete=models.PROTECT,
       related_name='order_lines'
   )
   quantity = models.DecimalField(max_digits=10, decimal_places=2)
   license_plate = models.ForeignKey(
       'inventory.Inventory',
       on_delete=models.PROTECT,
       related_name='order_lines',
       null=True,
       blank=True
   )
   serial_number = models.ForeignKey(
       'inventory.InventorySerialNumber',
       on_delete=models.PROTECT,
       related_name='order_lines',
       null=True,
       blank=True
   )
   lot = models.CharField(max_length=50, blank=True)
   vendor_lot = models.CharField(max_length=50, blank=True)
   notes = models.TextField(blank=True)

   class Meta:
       indexes = [
           models.Index(fields=['order', 'material']),
           models.Index(fields=['license_plate']),
           models.Index(fields=['serial_number']),
       ]

   def __str__(self):
       return f"Order {self.order.lookup_code_order} - {self.material.name} ({self.quantity})"