from rest_framework import serializers

from apps.shops.models import Shop
from apps.shops.products.models import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    shop_name = serializers.CharField(source='shop.name')

    class Meta:
        model = ProductCategory
        fields = (
            'id',
            'name',
            'icon',
            'shop_id',
            'shop_name'
        )

    def get_icon(self, obj):
        return obj.icon.url if obj.icon else None


class ProductCategorySimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = (
            'id',
            'name',
            'icon'
        )


class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False)
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.values_list('id', flat=True))

    class Meta:
        model = ProductCategory
        fields = (
            'name',
            'icon',
            'shop_id'
        )
