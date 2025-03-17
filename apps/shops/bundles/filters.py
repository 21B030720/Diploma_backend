from django_filters import rest_framework as filters

from apps.shops.bundles.models import Bundle


class BundleFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    from_price = filters.NumberFilter(method='filter_by_price_range')
    to_price = filters.NumberFilter(method='filter_by_price_range')

    class Meta:
        model = Bundle
        fields = {
        }

    def filter_by_price_range(self, queryset, name, value):
        if name == 'from_price':
            queryset = queryset.filter(price__gte=value)

        if name == 'to_price':
            queryset = queryset.filter(price__lte=value)

        return queryset