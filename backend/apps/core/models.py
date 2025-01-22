from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified' fields.
    """
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    createdByUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_created',
        null=True
    )
    modifiedByUser = models.ForeignKey(
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
    roleName = models.CharField(max_length=50, unique=True)
    permissions = models.JSONField(
        help_text="JSON field storing permitted actions"
    )

    def __str__(self):
        return self.roleName

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
    statusType = models.CharField(
        max_length=50,
        help_text="Entity this status applies to"
    )
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Statuses"
        unique_together = ['code', 'statusType']
        indexes = [
            models.Index(fields=['code', 'statusType']),
        ]

    def __str__(self):
        return f"{self.name} ({self.statusType})"

class Types(TimeStampedModel):
    """
    Flexible type management for various entities
    """
    entity = models.CharField(max_length=50)
    typeName = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Types"
        unique_together = ['entity', 'typeName']
        indexes = [
            models.Index(fields=['entity', 'typeName']),
        ]

    def __str__(self):
        return f"{self.typeName} ({self.entity})"

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
    isEnabled = models.BooleanField(default=False)
    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        default='global'
    )
    scopeID = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of customer/project if scoped"
    )

    class Meta:
        verbose_name_plural = "Feature Flags"
        indexes = [
            models.Index(fields=['scope', 'scopeID']),
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
    entityID = models.PositiveIntegerField()
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    userID = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='activity_logs'
    )

    class Meta:
        verbose_name_plural = "Logs"
        indexes = [
            models.Index(fields=['entity', 'entityID', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.action} on {self.entity} ({self.entityID})"

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
    entityID = models.PositiveIntegerField()
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    userID = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='audit_logs'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField()

    class Meta:
        verbose_name_plural = "Audit Logs"
        indexes = [
            models.Index(fields=['entity', 'entityID', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.action} on {self.entity} ({self.entityID})"