from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.activities.models import EventCategory, Event, Course, CourseCategory, CoursePriceList


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
            'social_networks',
            'location',
            'two_gis_link',
            'date_held',
            'from_age',
            'to_age'
        )


class EventCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=EventCategory.objects.values_list('id', flat=True))
    contacts = PhoneNumberField()

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
            'social_networks',
            'location',
            'two_gis_link',
            'date_held',
            'from_age',
            'to_age'
        )


class CourseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = (
            'id',
            'name',
            'description'
        )


class CourseCategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = (
            'name',
            'description'
        )


class CoursePriceListCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = CoursePriceList
        fields = (
            'id',
            'name',
            'description',
            'price',
            'payment_period'
        )


class CoursePriceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursePriceList
        fields = (
            'id',
            'name',
            'description',
            'price',
            'payment_period'
        )


class CourseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    course_prices = CoursePriceListSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'category_id',
            'category_name',
            'image',
            'description',
            'company',
            'contacts',
            'social_networks',
            'location',
            'two_gis_link',
            'from_age',
            'to_age',
            'course_prices'
        )


class CourseCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=CourseCategory.objects.values_list('id', flat=True))
    image = serializers.ImageField(required=False)
    course_prices = CoursePriceListCreateSerializer(many=True)
    contacts = PhoneNumberField()

    class Meta:
        model = Course
        fields = (
            'title',
            'category_id',
            'image',
            'description',
            'company',
            'contacts',
            'social_networks',
            'location',
            'two_gis_link',
            'from_age',
            'to_age',
            'course_prices'
        )

