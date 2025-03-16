from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from apps.reviews.models import ObjectRating
from apps.utils.enums import RatedObject


class RateSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        model = ObjectRating
        fields = (
            'rating',
            'review'
        )


class ObjectRatingSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='user.client_user.name')

    class Meta:
        model = ObjectRating
        fields = (
            'id',
            'client_name',
            'rating',
            'review',
            'status',
            'created_at',
            'changed_at'
        )


class ObjectRatingCRMSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='user.client_user.name')
    review_to = serializers.SerializerMethodField()
    review_to_name = serializers.SerializerMethodField()

    class Meta:
        model = ObjectRating
        fields = (
            'id',
            'client_name',
            'rating',
            'review',
            'status',
            'review_to',
            'review_to_name',
            'created_at',
            'changed_at',
            'service_provider',
            'product',
            'bundle',
            'course',
            'event',
            'shop',
        )

    def get_review_to(self, obj):
        if obj.service_provider:
            return RatedObject.SERVICE_PROVIDER
        elif obj.product:
            return RatedObject.PRODUCT
        elif obj.bundle:
            return RatedObject.BUNDLE
        elif obj.course:
            return RatedObject.COURSE
        elif obj.event:
            return RatedObject.EVENT
        elif obj.shop:
            return RatedObject.SHOP
        return None

    def get_review_to_name(self, obj):
        if obj.service_provider:
            return obj.service_provider.full_name
        elif obj.product:
            return obj.product.name
        elif obj.bundle:
            return obj.bundle.name
        elif obj.course:
            return obj.course.title
        elif obj.event:
            return obj.event.title
        elif obj.shop:
            return obj.shop.name
        return ''
