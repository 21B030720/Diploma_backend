from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.activities.models import EventCategory, Event, Course, CourseCategory, CoursePriceList
from apps.reviews.models import ObjectRating


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
    rating_from_user = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'avg_rating',
            'rating_from_user',
            'rating_count',
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

    @property
    def current_user(self):
        user = self.context.get('user', None)
        return user

    def get_rating_from_user(self, obj):
        if self.current_user:
            event_rating = ObjectRating.objects.filter(user=self.current_user,
                                                       event=obj).first()
            return event_rating.rating if event_rating else None
        return None


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
    rating_from_user = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'avg_rating',
            'rating_from_user',
            'rating_count',
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

    @property
    def current_user(self):
        user = self.context.get('user', None)
        return user

    def get_rating_from_user(self, obj):
        if self.current_user:
            event_rating = ObjectRating.objects.filter(user=self.current_user,
                                                       course=obj).first()
            return event_rating.rating if event_rating else None
        return None


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

