from django.contrib import admin
from .models import Status, Types, FeatureFlags, Logs, AuditLogs, Role

admin.site.register(Status)
admin.site.register(Types)
admin.site.register(FeatureFlags)
admin.site.register(Logs)
admin.site.register(AuditLogs)
admin.site.register(Role)