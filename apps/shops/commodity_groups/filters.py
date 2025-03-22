from django_filters import rest_framework as filters

from apps.shops.commodity_groups.models import CommodityGroup, CommodityGroupCategory


class CommodityGroupCategoryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = CommodityGroupCategory
        fields = {
        }


class CommodityGroupFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category_id = filters.NumberFilter(field_name='category_id', lookup_expr='exact')

    class Meta:
        model = CommodityGroup
        fields = {
        }
