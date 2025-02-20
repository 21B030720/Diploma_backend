from rest_framework import serializers

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
    image = serializers.SerializerMethodField()
    city_name = serializers.CharField(source='city.name')

    class Meta:
        model = Shop
        fields = (
            'id',
            'image',
            'name',
            'address',
            'blocked',
            'open_from',
            'open_until',
            'rating',
            'latitude',
            'longitude',
            'contacts',
            'city_id',
            'city_name',
            'two_gis_link',
        )

    def get_image(self, obj):
        return obj.image.url if obj.image else None


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
