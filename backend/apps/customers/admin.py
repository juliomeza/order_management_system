from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer, Project
from apps.core.admin import TimeStampedModelAdmin
from apps.core.models import Status

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'status', 'role', 'project'),
        }),
    )
    
    # Campos para edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role', 'status', 'project')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}), # Add it if needed: , 'groups', 'user_permissions'
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Si es un nuevo usuario
            form.base_fields['status'].initial = Status.objects.get(name="Active")
        return form
    
    # Método personalizado para mostrar nombre completo
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    # Campos visibles en la lista de usuarios
    list_display = ('full_name', 'email', 'role', 'status', 'project', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'full_name')
    ordering = ('first_name', 'last_name')
    list_filter = [] # Desactivar filtros automáticos

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0
    fields = ('name', 'lookup_code', 'orders_prefix', 'status')
    can_delete = False

@admin.register(Customer)
class CustomerAdmin(TimeStampedModelAdmin):
    list_display = ('name', 'lookup_code', 'status', 'output_format')
    search_fields = ('name', 'lookup_code')
    ordering = ('name',)
    inlines = [ProjectInline]
    #list_filter = ('status', 'output_format')

@admin.register(Project)
class ProjectAdmin(TimeStampedModelAdmin):
    list_display = ('name', 'lookup_code', 'orders_prefix', 'status', 'customer')
    search_fields = ('name', 'lookup_code', 'customer__name')
    ordering = ('name',)
    autocomplete_fields = ['contacts']
    #list_filter = ('status', 'customer', 'warehouse')
