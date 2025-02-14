import django_filters
from apps.inventory.models import Inventory
from apps.logistics.models import Contact

class InventoryFilter(django_filters.FilterSet):
    material_name = django_filters.CharFilter(field_name="material__name", lookup_expr="icontains")
    warehouse = django_filters.NumberFilter(field_name="warehouse_id")
    
    class Meta:
        model = Inventory
        fields = ["material_name", "warehouse"]

class ContactFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains")

    class Meta:
        model = Contact
        fields = ["name"]
