from rest_framework import serializers

from apps.reviews.models import ObjectRating
from apps.shops.models import Shop, City, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'id',
            'name'
        )


class CountryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'name',
        )


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'country',
        )


class CitySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'name'
        )


class CityCreateSerializer(serializers.ModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.values_list('id', flat=True))

    class Meta:
        model = City
        fields = (
            'name',
            'country_id'
        )


class ShopSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    city_name = serializers.CharField(source='city.name')
    rating_from_user = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = (
            'id',
            'image',
            'avg_rating',
            'rating_from_user',
            'rating_count',
            'name',
            'address',
            'blocked',
            'open_from',
            'open_until',
            'latitude',
            'longitude',
            'contacts',
            'city_id',
            'city_name',
            'two_gis_link',
        )

    @property
    def current_user(self):
        user = self.context.get('user', None)
        return user

    def get_rating_from_user(self, obj):
        if self.current_user:
            shop_rating = ObjectRating.objects.filter(user=self.current_user,
                                                                  shop=obj).first()
            return shop_rating.rating if shop_rating else None
        return None


class ShopSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            'id',
            'name'
        )


class ShopCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.values_list('id', flat=True))

    class Meta:
        model = Shop
        fields = (
            'name',
            'address',
            'image',
            'blocked',
            'open_from',
            'open_until',
            'latitude',
            'longitude',
            'contacts',
            'city_id',
            'two_gis_link'
        )
