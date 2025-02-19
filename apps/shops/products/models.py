from django.db import models

from apps.shops.commodity_groups.models import CommodityGroup
from apps.shops.models import Shop
from apps.utils.enums import Measures
from apps.utils.models import DeletedMixin, TimestampMixin


def upload_product_image(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'product_image', filename)


def upload_product_category_icon(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'product_category_icon', filename)


class ProductCategory(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to=upload_product_category_icon)
    shop = models.ForeignKey(Shop, related_name='categories', on_delete=models.CASCADE)


class ProductNutritionCharacteristics(DeletedMixin, TimestampMixin):
    nutritional_value = models.FloatField(default=0.0)
    fats = models.FloatField(default=0.0)
    proteins = models.FloatField(default=0.0)
    carbohydrates = models.FloatField(default=0.0)


class Product(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_product_image, null=True, blank=True)
    description = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE)
    nutrition_characteristics = models.ForeignKey(ProductNutritionCharacteristics,
                                                  related_name='products',
                                                  on_delete=models.SET_NULL,
                                                  null=True)
    from_age = models.IntegerField()
    to_age = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    measure = models.CharField(choices=Measures.choices, max_length=100)
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE)
    commodity_group = models.ForeignKey(CommodityGroup, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
