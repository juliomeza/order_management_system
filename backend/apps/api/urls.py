from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  
    TokenRefreshView,  
    TokenBlacklistView,  
)
from .views import get_or_create_orders, get_or_create_contacts, InventoryListView, ContactListView

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API de Ordenes y Logística",
        default_version='v1',
        description="Documentación de la API para gestionar órdenes, contactos e inventarios",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="soporte@example.com"),
        license=openapi.License(name="Licencia MIT"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Orders
    path('orders/', get_or_create_orders, name="get-orders"),

    # Auth endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Contacts
    path('contacts/', get_or_create_contacts, name='get-or-create-contacts'),
    path("contacts/list/", ContactListView.as_view(), name="contact-list"),

    # Inventory
    path("inventory/list/", InventoryListView.as_view(), name="inventory-list"),

    # Swagger Endpoints
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
