from rest_framework import serializers

from apps.shops.commodity_groups.models import CommodityGroupCategory, CommodityGroup
from apps.shops.models import Shop
from apps.shops.products.models import Product


class CommodityGroupCategoryCreateSerializer(serializers.ModelSerializer):
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.values_list('id', flat=True))
    icon = serializers.ImageField(required=False)

    class Meta:
        model = CommodityGroupCategory
        fields = (
            'name',
            'icon',
            'shop_id'
        )


class CommodityGroupCategorySerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name')

    class Meta:
        model = CommodityGroupCategory
        fields = (
            'id',
            'name',
            'icon',
            'shop_id',
            'shop_name'
        )


class CommodityGroupCategorySimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommodityGroupCategory
        fields = (
            'id',
            'name',
            'icon'
        )


class CommodityGroupCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.values_list('id', flat=True))
    category_id = serializers.PrimaryKeyRelatedField(queryset=CommodityGroupCategory.objects.values_list('id', flat=True))
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.values_list('id', flat=True),
                                                  many=True,
                                                  required=False)

    class Meta:
        model = CommodityGroup
        fields = (
            'name',
            'image',
            'description',
            'category_id',
            'shop_id',
            'products'
        )


class CommodityGroupSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    shop_name = serializers.CharField(source='shop.name')

    class Meta:
        model = CommodityGroup
        fields = (
            'id',
            'name',
            'image',
            'description',
            'category_id',
            'category_name',
            'shop_id',
            'shop_name'
        )
