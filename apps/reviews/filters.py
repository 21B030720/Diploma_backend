from django_filters import rest_framework as filters

from apps.reviews.models import ObjectRating


class ObjectRatingFilterSet(filters.FilterSet):
    type = filters.CharFilter(method='filter_by_type')
    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    from_rating = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    to_rating = filters.NumberFilter(field_name='rating', lookup_expr='lte')

    class Meta:
        model = ObjectRating
        fields = {
        }

    def filter_by_type(self, queryset, name, value):
        type_mapping = {
            'service_provider': 'service_provider',
            'product': 'product',
            'bundle': 'bundle',
            'course': 'course',
            'event': 'event',
            'shop': 'shop',
        }
        field_name = type_mapping.get(value.lower())
        if not field_name:
            return queryset
        filter_kwargs = {f'{field_name}__isnull': False}
        return queryset.filter(**filter_kwargs)
