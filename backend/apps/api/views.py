import logging
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema

# Models
from apps.orders.models import Order
from apps.logistics.models import Contact, CarrierService
from apps.inventory.models import Inventory

# Serializers
from .serializers import OrderSerializer, ContactSerializer, InventorySerializer, ProjectSerializer, WarehouseSerializer, CarrierSerializer, CarrierServiceSerializer

# Core Utilities
from apps.core.exceptions import BusinessLogicError
from apps.core.pagination import InventoryPagination, ContactsPagination
from apps.core.filters import InventoryFilter, ContactFilter

# Configure logger
logger = logging.getLogger('custom_logger')

@swagger_auto_schema(
    method='post',
    request_body=OrderSerializer
)
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

@swagger_auto_schema(
    method='post',
    request_body=ContactSerializer
)
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

### ✅ 5. API para Project
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_projects(request):
    """
    GET: Retrieves projects associated with the authenticated user.
    """
    user = request.user
    projects = user.project.customer.projects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


### ✅ 6. API para Warehouse
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_warehouses(request):
    """
    GET: Retrieves warehouses associated with the authenticated user's project.
    """
    user = request.user
    warehouses = user.project.warehouses.all()
    serializer = WarehouseSerializer(warehouses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

### ✅ 6. API para Carrier
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_carriers(request):
    """
    GET: Retrieves carriers available to the authenticated user's project.
    """
    user = request.user
    carriers = user.project.carriers.all()
    serializer = CarrierSerializer(carriers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

### ✅ 6. API para Carrier Service
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_carrier_services(request):
    """
    GET: Retrieves available carrier services based on the user's assigned carriers.
    If a carrier_id is provided, only returns services associated with that carrier.
    """
    user = request.user
    carrier_id = request.GET.get('carrier_id')

    if carrier_id:
        # Filtrar solo los CarrierService asociados al carrier_id y dentro del alcance del usuario
        carrier_services = CarrierService.objects.filter(
            carrier_id=carrier_id,
            carrier__in=user.project.carriers.all()
        )
    else:
        # Devolver todos los CarrierService disponibles para los carriers del usuario
        carrier_services = CarrierService.objects.filter(carrier__in=user.project.carriers.all())

    serializer = CarrierServiceSerializer(carrier_services, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

