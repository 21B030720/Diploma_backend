from django_filters import rest_framework as filters

from apps.shops.products.models import ProductCategory, Product


class ProductCategoryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    shop_id = filters.BaseInFilter(field_name='shop_id', lookup_expr='in')

    class Meta:
        model = ProductCategory
        fields = {
        }


class ProductFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    shop_id = filters.BaseInFilter(field_name='shop_id', lookup_expr='in')
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = {
            'category_id': ['exact'],
        }
