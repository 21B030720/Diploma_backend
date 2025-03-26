from rest_framework import serializers

from apps.reviews.models import ObjectRating
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
            'shop_name',
            'is_eatable'
        )

    # def get_icon(self, obj):
    #     return obj.icon.url if obj.icon else None


class ProductCategorySimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = (
            'id',
            'name',
            'icon',
            'is_eatable'
        )


class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False)
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.values_list('id', flat=True))

    class Meta:
        model = ProductCategory
        fields = (
            'name',
            'icon',
            'shop_id',
            'is_eatable'
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
    category_name = serializers.CharField(source='category.name', allow_null=True)
    nutrition_characteristics = NutritionCharacteristicsSerializer()
    rating_from_user = serializers.SerializerMethodField()
    commodity_group_name = serializers.CharField(source='commodity_group.name', allow_null=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'image',
            'avg_rating',
            'rating_from_user',
            'rating_count',
            'description',
            'category_id',
            'category_name',
            'nutrition_characteristics',
            'from_age',
            'to_age',
            'size',
            'price',
            'weight',
            'measure',
            'shop_id',
            'shop_name',
            'commodity_group',
            'commodity_group_name',
            'deleted'
        )

    @property
    def current_user(self):
        user = self.context.get('user', None)
        return user

    def get_rating_from_user(self, obj):
        if self.current_user:
            product_rating = ObjectRating.objects.filter(user=self.current_user,
                                                         product=obj).first()
            return product_rating.rating if product_rating else None
        return None


class ProductSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'deleted'
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    nutrition_characteristics = NutritionCharacteristicsCreateSerializer(required=False, allow_null=True)
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.values_list('id', flat=True))
    commodity_group_id = serializers.PrimaryKeyRelatedField(queryset=CommodityGroup.objects.values_list('id', flat=True),
                                                            required=False,
                                                            allow_null=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'image',
            'description',
            'commodity_group_id',
            'nutrition_characteristics',
            'from_age',
            'to_age',
            'size',
            'price',
            'weight',
            'measure',
            'shop_id',
        )
