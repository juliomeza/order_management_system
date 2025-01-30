from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from apps.orders.models import Order, OrderLine
from .serializers import OrderSerializer, OrderLineSerializer

@api_view(['GET', 'POST'])
def get_or_create_orders(request):
    """
    GET: Retorna la lista de órdenes en formato JSON.
    POST: Crea una nueva orden en la base de datos.
    """
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Guarda la nueva orden en la DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def get_or_create_order_lines(request):
    """
    GET: Retorna la lista de líneas de órdenes.
    POST: Crea una nueva línea de orden en la base de datos.
    """
    if request.method == 'GET':
        order_lines = OrderLine.objects.all()
        serializer = OrderLineSerializer(order_lines, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Guarda la nueva línea de orden en la DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)