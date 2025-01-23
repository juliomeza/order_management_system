from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified' fields.
    """
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_created',
        null=True
    )
    modified_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_modified',
        null=True
    )

    class Meta:
        abstract = True

class Role(TimeStampedModel):
    """
    Define user access levels and capabilities
    """
    role_name = models.CharField(max_length=50, unique=True)
    permissions = models.JSONField(
        help_text="JSON field storing permitted actions"
    )

    def __str__(self):
        return self.role_name

class Status(TimeStampedModel):
    """
    Centralized status management for all entities
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2)],
        help_text="Hierarchical structure code"
    )
    status_type = models.CharField(
        max_length=50,
        help_text="Entity this status applies to"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Statuses"
        unique_together = ['code', 'status_type']
        indexes = [
            models.Index(fields=['code', 'status_type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.status_type})"

class FeatureFlags(TimeStampedModel):
    """
    Feature toggle management
    """
    SCOPE_CHOICES = [
        ('global', 'Global'),
        ('customer', 'Customer'),
        ('project', 'Project'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=False)
    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        default='global'
    )
    scope_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of customer/project if scoped"
    )

    class Meta:
        verbose_name_plural = "Feature Flags"
        indexes = [
            models.Index(fields=['scope', 'scope_id']),
        ]

    def __str__(self):
        return self.name

class Logs(TimeStampedModel):
    """
    History table for system activities
    """
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    entity = models.CharField(max_length=50)
    entity_id = models.PositiveIntegerField()
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='activity_logs'
    )

    class Meta:
        verbose_name_plural = "Logs"
        indexes = [
            models.Index(fields=['entity', 'entity_id', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.action} on {self.entity} ({self.entity_id})"

class AuditLogs(TimeStampedModel):
    """
    System-wide change tracking
    """
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    entity = models.CharField(max_length=50)
    entity_id = models.PositiveIntegerField()
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='audit_logs'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField()

    class Meta:
        verbose_name_plural = "Audit Logs"
        indexes = [
            models.Index(fields=['entity', 'entity_id', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.action} on {self.entity} ({self.entity_id})"