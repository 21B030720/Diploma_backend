from django_filters import rest_framework as filters

from apps.services.models import ServiceCategory, Service


class ServiceCategoryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ServiceCategory
        fields = {
        }


class ServiceFilterSet(filters.FilterSet):
    title = filters.CharFilter(field_name='name', lookup_expr='icontains')
    service_type = filters.CharFilter(field_name='service_type', lookup_expr='exact')

    class Meta:
        model = Service
        fields = {

        }
