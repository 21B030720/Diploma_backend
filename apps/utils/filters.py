from django.db.models import CharField, TextField
from django.db.models.functions import Lower
from rest_framework.filters import BaseFilterBackend


class SortingFilterBackend(BaseFilterBackend):
    ordering_param = 'sort'

    def filter_queryset(self, request, queryset, view):
        sort_query = request.query_params.getlist('sort')
        order_fields = []
        if len(sort_query) > 0:
            has_sorting_fields = hasattr(view, 'sorting_fields')
            for field in sort_query:
                sort_field = field.split()[0].lower()
                is_desc = field.split()[1] == 'desc'
                order_by = sort_field
                if has_sorting_fields:
                    if sort_field in view.sorting_fields:
                        order_by = view.sorting_fields[sort_field]
                try:
                    field_class = type(queryset.model._meta.get_field(order_by))
                except Exception as e:
                    field_class = None
                if field_class or '__' in order_by:
                    if field_class in [CharField, TextField]:
                        order_by = Lower(order_by).desc() if is_desc else Lower(order_by)
                    else:
                        order_by = f"-{order_by}" if is_desc else order_by
                    order_fields.append(order_by)
            queryset = queryset.order_by(*order_fields)
        return queryset
