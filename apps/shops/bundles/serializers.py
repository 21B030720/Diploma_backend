from rest_framework import serializers

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
            'products',
            'shop_id',
            'discount'
        )


class BundleSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name')

    class Meta:
        model = Bundle
        fields = (
            'id',
            'name',
            'shop_id',
            'shop_name',
            'discount',
            'price'
        )


class BundleDetailSerializer(BundleSerializer):
    products = ProductSimpleSerializer(many=True)

    class Meta:
        model = Bundle
        fields = BundleSerializer.Meta.fields + (
            'products',
        )
