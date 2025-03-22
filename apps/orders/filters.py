from django_filters import rest_framework as filters

from apps.orders.models import ClientOrder, OrderItem
from apps.reviews.models import ObjectRating


class ClientOrderFilterSet(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = ClientOrder
        fields = {
        }


class OrderItemFilterSet(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    item_type = filters.CharFilter(field_name='item_type', lookup_expr='exact')

    class Meta:
        model = OrderItem
        fields = {
        }
