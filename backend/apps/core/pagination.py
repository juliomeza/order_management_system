from rest_framework.pagination import CursorPagination

class InventoryPagination(CursorPagination):
    page_size = 20
    ordering = 'id'

class ContactsPagination(CursorPagination):
    page_size = 20
    ordering = "first_name"  # Ordenar por nombre del contacto
