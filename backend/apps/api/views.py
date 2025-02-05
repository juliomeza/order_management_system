import logging
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Models
from apps.orders.models import Order
from apps.logistics.models import Contact
from apps.inventory.models import Inventory

# Serializers
from .serializers import OrderSerializer, ContactSerializer, InventorySerializer

# Core Utilities
from apps.core.exceptions import BusinessLogicError
from apps.core.pagination import InventoryPagination, ContactsPagination
from apps.core.filters import InventoryFilter, ContactFilter

# Configure logger
logger = logging.getLogger('custom_logger')


### ✅ 1. API para Ordenes
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_orders(request):
    """
    GET: Retrieves only the orders that belong to the authenticated user's customer.
    POST: Creates a new order only if the user is allowed to create it within their customer and project.
    """
    user = request.user

    if request.method == 'GET':
        orders = Order.objects.filter(project__customer=user.project.customer)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        if data.get("project") and int(data["project"]) != user.project.id:
            raise BusinessLogicError(detail="You can only create orders for your assigned project.")

        serializer = OrderSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            logger.info(f"Order successfully created: {order.lookup_code_order}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        raise BusinessLogicError(detail=serializer.errors)


### ✅ 2. API para Contactos
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_contacts(request):
    """
    GET: Retrieves all contacts associated with the authenticated user's project.
    POST: Allows a user to create a contact for their assigned project.
    """
    user = request.user

    if request.method == 'GET':
        contacts = user.project.contacts.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            contact = serializer.save()
            logger.info(f"Contact successfully created: {contact.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        raise BusinessLogicError(detail=serializer.errors)


### ✅ 3. API para Inventario con paginación y búsqueda en tiempo real
class InventoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    pagination_class = InventoryPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = InventoryFilter
    search_fields = ["material__name"]  # Búsqueda en el nombre del material


### ✅ 4. API para Contactos con paginación y búsqueda en tiempo real
class ContactListView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = ContactsPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ContactFilter
    search_fields = ["first_name", "last_name", "email"]  # Búsqueda en nombre y correo
