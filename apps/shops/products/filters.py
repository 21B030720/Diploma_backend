from django_filters import rest_framework as filters

from apps.shops.products.models import ProductCategory, Product


class ProductCategoryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ProductCategory
        fields = {
            'shop_id': ['exact']
        }


class ProductFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = {
            'shop_id': ['exact'],
            'category_id': ['exact'],
        }
