import logging
from apps.orders.models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# Configure logger
logger = logging.getLogger('custom_logger')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_orders(request):
    """
    GET: Retrieves the list of orders in JSON format.
    - Requires authentication.
    - Returns all orders along with their related line items.

    POST: Creates a new order in the database.
    - Requires authentication.
    - Validates and saves the order if the request data is correct.
    """
    try:
        if request.method == 'GET':
            orders = Order.objects.prefetch_related('lines').all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Order successfully created: {serializer.data}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Validation error when creating order: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error in get_or_create_orders: {str(e)}", exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)