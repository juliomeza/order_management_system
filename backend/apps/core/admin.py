from django.contrib import admin
from .models import Status, FeatureFlags, Logs, AuditLogs, Role

class TimeStampedModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by_user', 'modified_by_user', 'created_date', 'modified_date')
    
    def save_model(self, request, obj, form, change):
        obj._current_user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Status)
class StatusAdmin(TimeStampedModelAdmin):
    list_display = ('name', 'code', 'status_type', 'is_active')
    search_fields = ('name', 'code', 'status_type')
    ordering = ('status_type', 'name',)
    #list_filter = ('is_active', 'status_type')

@admin.register(FeatureFlags)
class FeatureFlagsAdmin(TimeStampedModelAdmin):
    list_display = ('name', 'is_enabled', 'scope')
    search_fields = ('name', 'scope')
    ordering = ('name',)
    #list_filter = ('is_enabled', 'scope')

@admin.register(Logs)
class LogsAdmin(TimeStampedModelAdmin):
    list_display = ('entity', 'entity_id', 'action', 'timestamp')
    search_fields = ('entity', 'entity_id', 'action')
    ordering = ('-timestamp',)
    #list_filter = ('action',)

@admin.register(AuditLogs)
class AuditLogsAdmin(TimeStampedModelAdmin):
    list_display = ('entity', 'entity_id', 'action', 'timestamp', 'user_id')
    search_fields = ('entity', 'entity_id', 'action', 'user_id__email')
    ordering = ('-timestamp',)
    #list_filter = ('action',)

@admin.register(Role)
class RoleAdmin(TimeStampedModelAdmin):
    list_display = ('role_name',)
    search_fields = ('role_name',)
    ordering = ('role_name',)