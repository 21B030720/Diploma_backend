from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from apps.shops.products.models import ProductCategory, Product


class ProductCategoryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ProductCategory
        fields = {
        }


class ProductFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category_id = filters.NumberFilter(field_name='category_id', lookup_expr='exact')
    from_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    to_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = {
        }

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        search_from = self.data.get('from_age')
        search_to = self.data.get('to_age')

        if search_from and search_to:
            try:
                search_from = int(search_from)
                search_to = int(search_to)
            except ValueError:
                raise ValidationError("Provide numeric value")

            # record.from_age <= search_to AND record.to_age >= search_from
            queryset = queryset.filter(from_age__lte=search_to, to_age__gte=search_from)

        elif search_from:
            try:
                search_from = int(search_from)
            except ValueError:
                raise ValidationError("Provide numeric value")
            queryset = queryset.filter(to_age__gte=search_from)

        elif search_to:
            try:
                search_to = int(search_to)
            except ValueError:
                raise ValidationError("Provide numeric value")
            queryset = queryset.filter(from_age__lte=search_to)

        return queryset
