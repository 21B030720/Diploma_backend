from rest_framework.generics import get_object_or_404

from apps.shops.products.models import Product, ProductCategory


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
    product_category.save()
