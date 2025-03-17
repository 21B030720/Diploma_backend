from rest_framework import serializers

from apps.reviews.models import ObjectRating
from apps.shops.bundles.models import Bundle
from apps.shops.models import Shop
from apps.shops.products.models import Product
from apps.shops.products.serializers import ProductSimpleSerializer


class BundleCreateSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.values_list('id', flat=True), many=True)
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.values_list('id', flat=True))

    class Meta:
        model = Bundle
        fields = (
            'name',
            'description',
            'products',
            'shop_id',
            'discount'
        )


class BundleSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name')
    rating_from_user = serializers.SerializerMethodField()

    class Meta:
        model = Bundle
        fields = (
            'id',
            'name',
            'description',
            'avg_rating',
            'rating_from_user',
            'rating_count',
            'shop_id',
            'shop_name',
            'discount',
            'price'
        )

    @property
    def current_user(self):
        user = self.context.get('user', None)
        return user

    def get_rating_from_user(self, obj):
        if self.current_user:
            bundle_rating = ObjectRating.objects.filter(user=self.current_user,
                                                        bundle=obj).first()
            return bundle_rating.rating if bundle_rating else None
        return None


class BundleDetailSerializer(BundleSerializer):
    products = ProductSimpleSerializer(many=True)

    class Meta:
        model = Bundle
        fields = BundleSerializer.Meta.fields + (
            'products',
        )
