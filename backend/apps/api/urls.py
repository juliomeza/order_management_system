from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  
    TokenRefreshView,  
    TokenBlacklistView,  
)
from .views import (
    get_or_create_orders,
    get_or_create_contacts,
    InventoryListView,
    ContactListView,
    get_projects,
    get_warehouses,
    get_carriers,
    get_carrier_services,
    UserDetailView,
)

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
    authentication_classes=[],
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

    path('warehouses/', get_warehouses, name='get-warehouses'),
    path('projects/', get_projects, name='get-projects'),
    path('carriers/', get_carriers, name='get-carriers'),
    path('carrier-services/', get_carrier_services, name='get-carrier-services'),

    # User
    path("users/me/", UserDetailView.as_view(), name="user-detail"),

    # Swagger Endpoints
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
