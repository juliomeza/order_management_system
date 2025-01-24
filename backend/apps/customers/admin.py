from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer, Project

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Campos para edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role', 'status', 'project')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}), # Add it if needed: , 'groups', 'user_permissions'
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Método personalizado para mostrar nombre completo
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    # Campos visibles en la lista de usuarios
    list_display = ('project', 'full_name', 'email', 'role', 'status', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'full_name')
    ordering = ('project', 'email',)
    list_filter = [] # Desactivar filtros automáticos

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'lookup_code', 'status', 'output_format')
    search_fields = ('name', 'lookup_code')
    ordering = ('name',)
    #list_filter = ('status', 'output_format')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('customer', 'name', 'lookup_code', 'orders_prefix', 'status')
    search_fields = ('name', 'lookup_code', 'customer__name')
    ordering = ('customer', 'name',)
    #list_filter = ('status', 'customer', 'warehouse')
