from django.contrib import admin
from .models import User, Roles, Customers, Projects, Status, Addresses

admin.site.register(User)
admin.site.register(Roles)
admin.site.register(Customers)
admin.site.register(Projects)
admin.site.register(Status)
admin.site.register(Addresses)
