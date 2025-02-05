from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Para obtener access y refresh token
    TokenRefreshView,  # Para refrescar el token de acceso
    TokenBlacklistView,  # Para hacer logout
)
from .views import get_or_create_orders, get_or_create_contacts, InventoryListView, ContactListView

urlpatterns = [
    # Orders
    path('orders/', get_or_create_orders, name="get-orders"),

    # Auth endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),  # Logout

    # Contacts
    path('contacts/', get_or_create_contacts, name='get-or-create-contacts'),
    path("contacts/list/", ContactListView.as_view(), name="contact-list"),

    # Inventory
    path("inventory/list/", InventoryListView.as_view(), name="inventory-list"),
]
