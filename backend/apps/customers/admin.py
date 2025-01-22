from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer, Project

class CustomUserAdmin(BaseUserAdmin):
    # Campos para edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role', 'status', 'project')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}), # Add it if needed: , 'groups', 'user_permissions'
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Campos visibles en la lista de usuarios
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    # Habilitar búsqueda
    search_fields = ('email', 'first_name', 'last_name')
    # Definir orden
    ordering = ('email',)
    # Desactivar filtros automáticos
    list_filter = []

# Personalización de CustomerAdmin
class CustomerAdmin(admin.ModelAdmin):
    # Campos visibles en la tabla
    list_display = ('name', 'lookup_code', 'status', 'output_format')
    # Campos habilitados para búsqueda
    search_fields = ('name', 'lookup_code')
    # Orden por defecto
    ordering = ('name',)
    # Filtros laterales
    #list_filter = ('status', 'output_format')

class ProjectAdmin(admin.ModelAdmin):
    # Campos visibles en la tabla
    list_display = ('name', 'lookup_code', 'customer', 'status', 'warehouse')
    # Campos habilitados para búsqueda
    search_fields = ('name', 'lookup_code', 'customer__name')
    # Orden por defecto
    ordering = ('name',)
    # Filtros laterales
    #list_filter = ('status', 'customer', 'warehouse')

# Re-registrar el modelo User
admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Project, ProjectAdmin)
