from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from apps.activities.models import CourseCategory, Course, EventCategory, Event


class EventCategoryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = EventCategory
        fields = {
        }


class EventFilterSet(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    from_price = filters.NumberFilter(method='filter_by_price_range')
    to_price = filters.NumberFilter(method='filter_by_price_range')

    class Meta:
        model = Event
        fields = {

        }

    def filter_by_price_range(self, queryset, name, value):
        if name == 'from_price':
            queryset = queryset.filter(price__gte=value)

        if name == 'to_price':
            queryset = queryset.filter(price__lte=value)

        return queryset

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


class CourseCategoryFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = CourseCategory
        fields = {
        }


class CourseFilterSet(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Course
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
