from django_filters import rest_framework as filters

from apps.shops.models import Shop, City, Country


class CountryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Country
        fields = {
        }


class CityFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = City
        fields = {
        }


class ShopFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Shop
        fields = {
            'address': ['icontains'],
            'city_id': ['exact']
        }
