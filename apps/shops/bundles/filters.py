from django_filters import rest_framework as filters

from apps.shops.bundles.models import Bundle


class BundleFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    shop_id = filters.BaseInFilter(field_name='shop_id', lookup_expr='in')

    class Meta:
        model = Bundle
        fields = {
        }
