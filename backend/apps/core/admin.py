from django.contrib import admin
from .models import Status, Types, FeatureFlags, Logs, AuditLogs, Role

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status_type', 'is_active')
    search_fields = ('name', 'code', 'status_type')
    ordering = ('status_type', 'name',)
    #list_filter = ('is_active', 'status_type')

@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'entity', 'is_active')
    search_fields = ('type_name', 'entity')
    ordering = ('entity', 'type_name')
    #list_filter = ('is_active',)

@admin.register(FeatureFlags)
class FeatureFlagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enabled', 'scope')
    search_fields = ('name', 'scope')
    ordering = ('name',)
    #list_filter = ('is_enabled', 'scope')

@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('entity', 'entity_id', 'action', 'timestamp')
    search_fields = ('entity', 'entity_id', 'action')
    ordering = ('-timestamp',)
    #list_filter = ('action',)

@admin.register(AuditLogs)
class AuditLogsAdmin(admin.ModelAdmin):
    list_display = ('entity', 'entity_id', 'action', 'timestamp', 'user_id')
    search_fields = ('entity', 'entity_id', 'action', 'user_id__email')
    ordering = ('-timestamp',)
    #list_filter = ('action',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)
    search_fields = ('role_name',)
    ordering = ('role_name',)