from django_filters import rest_framework as filters

from apps.shops.bundles.models import Bundle


class BundleFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    from_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    to_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Bundle
        fields = {
        }
