from django_filters import rest_framework as filters

from apps.shops.commodity_groups.models import CommodityGroup, CommodityGroupCategory


class CommodityGroupCategoryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    shop_id = filters.BaseInFilter(field_name='shop_id', lookup_expr='in')

    class Meta:
        model = CommodityGroupCategory
        fields = {
        }


class CommodityGroupFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    shop_id = filters.BaseInFilter(field_name='shop_id', lookup_expr='in')
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = CommodityGroup
        fields = {
            'category_id': ['exact']
        }