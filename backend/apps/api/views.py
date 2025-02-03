import logging
from apps.orders.models import Order
from apps.logistics.models import Contact
from .serializers import OrderSerializer, ContactSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from apps.core.exceptions import BusinessLogicError

# Configure logger
logger = logging.getLogger('custom_logger')

# Get or create orders
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_orders(request):
    """
    GET: Retrieves only the orders that belong to the authenticated user's customer.
    POST: Creates a new order only if the user is allowed to create it within their customer and project.
    """
    user = request.user

    if request.method == 'GET':
        # ✅ Retrieve only orders for the authenticated user's customer
        orders = Order.objects.filter(project__customer=user.project.customer)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data

        # ✅ Restrict creation to only allowed projects
        if data.get("project") and int(data["project"]) != user.project.id:
            raise BusinessLogicError(detail="You can only create orders for your assigned project.")

        serializer = OrderSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            logger.info(f"Order successfully created: {order.lookup_code_order}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        raise BusinessLogicError(detail=serializer.errors)  # Use standardized error


# Get or create contacts
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_contacts(request):
    """
    GET: Retrieves all contacts associated with the authenticated user's project.
    POST: Allows a user to create a contact for their assigned project.
    """
    user = request.user

    if request.method == 'GET':
        # ✅ Retrieve all contacts linked to the user's project
        contacts = user.project.contacts.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # ✅ Create a new contact
        serializer = ContactSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            contact = serializer.save()
            logger.info(f"Contact successfully created: {contact.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        raise BusinessLogicError(detail=serializer.errors)  # Use standardized error
