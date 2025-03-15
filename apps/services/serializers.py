from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from apps.services.models import ServiceCategory, Service, ServiceProvider, ServiceProviderRating


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = (
            'id',
            'name',
            'description',
            'icon'
        )


class ServiceCategoryCreateSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False)

    class Meta:
        model = ServiceCategory
        fields = (
            'name',
            'description',
            'icon'
        )


class ServiceProviderSerializer(serializers.ModelSerializer):
    rating_from_user = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProvider
        fields = (
            'id',
            'full_name',
            'profile_photo',
            'phone_number',
            'email',
            'social_networks',
            'resume',
            'is_active',
            'avg_rating',
            'rating_from_user',
            'rating_count'
        )

    @property
    def current_user(self):
        user = self.context.get('user', None)
        return user

    def get_rating_from_user(self, obj):
        if self.current_user:
            service_provider_rating = ServiceProviderRating.objects.filter(user=self.current_user,
                                                          service_provider=obj).first()
            return service_provider_rating.rating if service_provider_rating else None
        return None


class ServiceProviderCreateSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)
    resume = serializers.FileField(required=False)

    class Meta:
        model = ServiceProvider
        fields = (
            'full_name',
            'profile_photo',
            'phone_number',
            'email',
            'social_networks',
            'resume',
            'is_active'
        )


class RateProviderSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        model = ServiceProviderRating
        fields = (
            'rating',
        )


class ServiceSerializer(serializers.ModelSerializer):
    service_provider = ServiceProviderSerializer()
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Service
        fields = (
            'id',
            'title',
            'category_id',
            'category_name',
            'service_provider',
            'service_type',
            'address',
            'price',
            'payment_period'
        )


class ServiceCreateSerializer(serializers.ModelSerializer):
    service_provider = ServiceProviderCreateSerializer()
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.values_list('id', flat=True)
    )

    class Meta:
        model = Service
        fields = (
            'id',
            'title',
            'category_id',
            'service_provider',
            'service_type',
            'address',
            'price',
            'payment_period',
        )
