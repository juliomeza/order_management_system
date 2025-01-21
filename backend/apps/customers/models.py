from django.contrib.auth.models import AbstractUser
from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Addresses(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('Projects', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey('Roles', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
    modified_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_users')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )


class Roles(models.Model):
    role_name = models.CharField(max_length=100, unique=True)
    permissions = models.JSONField()  # Ejemplo: {"can_view": True, "can_edit": False}
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_roles')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_roles')


class Customers(models.Model):
    name = models.CharField(max_length=255)
    lookup_code = models.CharField(max_length=100, unique=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Addresses, on_delete=models.SET_NULL, null=True, blank=True)
    output_format = models.CharField(max_length=10, choices=[('CSV', 'CSV'), ('JSON', 'JSON')])
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_customers')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_customers')


class Projects(models.Model):
    name = models.CharField(max_length=255)
    lookup_code = models.CharField(max_length=100, unique=True)
    orders_prefix = models.CharField(max_length=50, unique=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='projects')
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_projects')
