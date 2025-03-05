from django_filters import rest_framework as filters

from apps.users.models import CRMUser, ClientUser


class CRMUserFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = CRMUser
        fields = {
            'shop_id': ['exact'],
            'role': ['exact']
        }


class ClientUserFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    phone = filters.CharFilter(field_name='phone', lookup_expr='icontains')

    class Meta:
        models = ClientUser
        fields = {
        }
