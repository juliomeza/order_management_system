from django.contrib import admin
from .models import User, Role, Customer, Project

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Customer)
admin.site.register(Project)