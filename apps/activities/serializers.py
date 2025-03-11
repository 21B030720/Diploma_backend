from rest_framework import serializers

from apps.activities.models import EventCategory, Event


class EventCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCategory
        fields = (
            'id',
            'name',
            'description'
        )


class EventCategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCategory
        fields = (
            'name',
            'description'
        )


class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'category_id',
            'category_name',
            'image',
            'description',
            'price',
            'tickets_left',
            'organizator',
            'contacts',
            'location',
            'two_gis_link',
            'date_held',
            'from_age',
            'to_age'
        )


class EventCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=EventCategory.objects.values_list('id', flat=True))

    class Meta:
        model = Event
        fields = (
            'title',
            'category_id',
            'image',
            'description',
            'price',
            'tickets_left',
            'organizator',
            'contacts',
            'location',
            'two_gis_link',
            'date_held',
            'from_age',
            'to_age'
        )
