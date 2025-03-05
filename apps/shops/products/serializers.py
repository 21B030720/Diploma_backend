from rest_framework import serializers

from apps.shops.commodity_groups.models import CommodityGroup
from apps.shops.models import Shop
from apps.shops.products.models import ProductCategory, Product, ProductNutritionCharacteristics


class ProductCategorySerializer(serializers.ModelSerializer):
    # icon = serializers.SerializerMethodField()
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

    # def get_icon(self, obj):
    #     return obj.icon.url if obj.icon else None


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


class NutritionCharacteristicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductNutritionCharacteristics
        fields = (
            'nutritional_value',
            'fats',
            'proteins',
            'carbohydrates'
        )


class NutritionCharacteristicsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductNutritionCharacteristics
        fields = (
            'nutritional_value',
            'fats',
            'proteins',
            'carbohydrates'
        )


class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name')
    category_name = serializers.CharField(source='category.name')
    nutrition_characteristics = NutritionCharacteristicsSerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'image',
            'description',
            'rating',
            'category_id',
            'category_name',
            'nutrition_characteristics',
            'from_age',
            'to_age',
            'price',
            'measure',
            'shop_id',
            'shop_name',
            'commodity_group'
        )


class ProductSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'name'
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    category_id = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.values_list('id', flat=True))
    nutrition_characteristics = NutritionCharacteristicsCreateSerializer(required=False, allow_null=True)
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.values_list('id', flat=True))
    commodity_group_id = serializers.PrimaryKeyRelatedField(queryset=CommodityGroup.objects.values_list('id', flat=True), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'image',
            'description',
            'category_id',
            'nutrition_characteristics',
            'from_age',
            'to_age',
            'price',
            'measure',
            'shop_id',
            'commodity_group_id'
        )
