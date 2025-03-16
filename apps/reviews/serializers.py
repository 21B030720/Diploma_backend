from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from apps.reviews.models import ObjectRating


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
            'created_at',
            'changed_at'
        )