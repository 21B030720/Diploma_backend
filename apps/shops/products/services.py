from django.db import transaction
from rest_framework.generics import get_object_or_404

from apps.shops.products.models import Product, ProductCategory, ProductNutritionCharacteristics


def add_product_category(data):
    product_category = ProductCategory.objects.create(**data)
    return product_category


def update_product_category(pk, data):
    product_category = get_object_or_404(ProductCategory, pk=pk)

    for key, value in data.items():
        setattr(product_category, key, value)

    product_category.save()
    return product_category


def delete_product_category(pk):
    product_category = get_object_or_404(ProductCategory, pk=pk)
    product_category.deleted = True
    product_category.save(update_fields=['deleted'])


def create_nutrition_characteristics(data):
    if data is None:
        nutrition_characteristics = ProductNutritionCharacteristics.objects.create()
    else:
        nutrition_characteristics = ProductNutritionCharacteristics.objects.create(**data)
    return nutrition_characteristics


@transaction.atomic
def add_product(data):
    nutrition_characteristics_data = data.pop('nutrition_characteristics', None)
    nutrition_characteristics = create_nutrition_characteristics(nutrition_characteristics_data)
    data['nutrition_characteristics_id'] = nutrition_characteristics.id
    product = Product.objects.create(**data)
    return product


def update_product(pk, data):
    product = get_object_or_404(Product, pk=pk)
    nutrition_characteristics_data = data.pop('nutrition_characteristics', None)
    nutrition_characteristics = product.nutrition_characteristics
    for key, value in nutrition_characteristics_data.items():
        setattr(nutrition_characteristics, key, value)
    nutrition_characteristics.save()

    for key, value in data.items():
        setattr(product, key, value)
    product.save()
    return product


def delete_product(pk):
    product = get_object_or_404(Product, pk=pk)
    product.deleted = True
    product.save(update_fields=['deleted'])
