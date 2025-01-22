from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from apps.core.models import Status, Role

class Customer(models.Model):
    """
    Root entity for multi-tenant structure
    """
    OUTPUT_FORMAT_CHOICES = [
        ('CSV', 'CSV'),
        ('JSON', 'JSON'),
    ]

    name = models.CharField(max_length=100)
    lookupCode = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='customers'
    )
    # addressID will be added when we create the Logistics app
    address = models.ForeignKey(
        'logistics.Address',
        on_delete=models.PROTECT,
        related_name='customers',
        null=True
    )
    outputFormat = models.CharField(
        max_length=4,
        choices=OUTPUT_FORMAT_CHOICES,
        default='JSON'
    )
    notes = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='customers_created',
        null=True
    )
    modified_by = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='customers_modified',
        null=True
    )

    def __str__(self):
        return f"{self.name} ({self.lookupCode})"

class Project(models.Model):
    """
    Organize customer operations
    """
    name = models.CharField(max_length=100)
    lookupCode = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    ordersPrefix = models.CharField(
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
    notes = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='projects_created',
        null=True
    )
    modified_by = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='projects_modified',
        null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['customer', 'status']),
        ]

    def __str__(self):
        return f"{self.name} ({self.customer.name})"

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    """
    first_name = models.CharField(max_length=30)  # Changed from firstName
    last_name = models.CharField(max_length=30)   # Changed from lastName
    email = models.EmailField(unique=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='users',
        null=True
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