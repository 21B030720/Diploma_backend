from rest_framework.generics import get_object_or_404

from apps.shops.bundles.models import Bundle


def add_bundle(data):
    products = data.pop('products', [])
    bundle = Bundle.objects.create(**data)
    bundle.products.set(products)
    return bundle


def update_bundle(pk, data):
    products = data.pop('products', [])
    bundle = get_object_or_404(Bundle, pk=pk)

    for key, value in data.items():
        setattr(bundle, key, value)

    bundle.save()
    bundle.products.set(products)
    return bundle


def delete_bundle(pk):
    bundle = get_object_or_404(Bundle, pk=pk)
    bundle.deleted = True
    bundle.save(update_fields=['deleted'])
