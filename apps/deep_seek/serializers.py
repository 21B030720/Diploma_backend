from rest_framework import serializers

from apps.shops.commodity_groups.models import CommodityGroupCategory, CommodityGroup
from apps.shops.models import Shop
from apps.shops.products.models import Product
from apps.shops.products.serializers import NutritionCharacteristicsSerializer


class ProductHeavyInfoSerializer(serializers.ModelSerializer):
    nutrition_characteristics = NutritionCharacteristicsSerializer()
    commodity_group_name = serializers.CharField(source='commodity_group_name.name')

    class Meta:
        model = Product
        fields = (
            'name',
            'commodity_group_name',
            'description',
            'from_age',
            'to_age',
            'price',
            'measure',
            'nutrition_characteristics'
        )


class CommodityGroupHeavyInfoSerializer(serializers.ModelSerializer):
    products_in_this_group = ProductHeavyInfoSerializer(source='products', many=True)

    class Meta:
        model = CommodityGroup
        fields = (
            'name',
            'description',
            'products_in_this_group'
        )


class CommodityGroupCategoryHeavyInfoSerializer(serializers.ModelSerializer):
    commodity_groups_inside_this_category = CommodityGroupHeavyInfoSerializer(source='commodity_groups', many=True)

    class Meta:
        model = CommodityGroupCategory
        fields = (
            'name',
            'commodity_groups_inside_this_category'
        )


class ShopsHeavyInfoSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='name')
    commodity_group_categories_available_in_this_shop = CommodityGroupCategoryHeavyInfoSerializer(
        source='commodity_group_categories',
        many=True
    )
    located_city = serializers.CharField(source='city.name')
    located_country = serializers.CharField(source='city.country.name')

    class Meta:
        model = Shop
        fields = (
            'shop_name',
            'address',
            'located_country',
            'located_city',
            'commodity_group_categories_available_in_this_shop'
        )


class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField()