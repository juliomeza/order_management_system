import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from apps.orders.models import Order, OrderLine
from .serializers import OrderSerializer, OrderLineSerializer

# Configure logger
logger = logging.getLogger('custom_logger')

@api_view(['GET', 'POST'])
def get_or_create_orders(request):
    """
    GET: Returns the list of orders in JSON format.
    POST: Creates a new order in the database.
    """
    try:
        if request.method == 'GET':
            orders = Order.objects.all()
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

@api_view(['GET', 'POST'])
def get_or_create_order_lines(request):
    """
    GET: Returns the list of order lines.
    POST: Creates a new order line in the database.
    """
    try:
        if request.method == 'GET':
            order_lines = OrderLine.objects.all()
            serializer = OrderLineSerializer(order_lines, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = OrderLineSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Order line successfully created: {serializer.data}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Validation error when creating order line: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error in get_or_create_order_lines: {str(e)}", exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
