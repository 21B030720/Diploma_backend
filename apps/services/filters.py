from django_filters import rest_framework as filters

from apps.services.models import ServiceCategory, Service


class ServiceCategoryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ServiceCategory
        fields = {
        }


class ServiceFilterSet(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    service_type = filters.CharFilter(field_name='service_type', lookup_expr='exact')
    category_id = filters.NumberFilter(field_name='category_id', lookup_expr='exact')
    from_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    to_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Service
        fields = {
        }
