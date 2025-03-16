from django.db.models import Sum
from rest_framework.generics import get_object_or_404

from apps.reviews.models import ObjectRating
from apps.shops.bundles.models import Bundle


def add_bundle(data):
    products = data.pop('products', [])
    discount = data.get('discount', 0)
    bundle = Bundle.objects.create(**data)
    bundle.products.set(products)
    total_price_of_products = bundle.products.aggregate(total_price=Sum('price'))['total_price']
    bundle_price = total_price_of_products * (100 - discount) / 100
    bundle.price = bundle_price
    bundle.save(update_fields=['price'])
    return bundle


def update_bundle(pk, data):
    products = data.pop('products', [])
    discount = data.get('discount', 0)
    bundle = get_object_or_404(Bundle, pk=pk)

    for key, value in data.items():
        setattr(bundle, key, value)

    bundle.products.set(products)

    total_price_of_products = bundle.products.aggregate(total_price=Sum('price'))['total_price']
    bundle_price = total_price_of_products * (100 - discount) / 100
    bundle.price = bundle_price
    bundle.save()
    return bundle


def delete_bundle(pk):
    bundle = get_object_or_404(Bundle, pk=pk)
    bundle.deleted = True
    bundle.save(update_fields=['deleted'])


def rate_bundle(bundle, user, data):
    is_already_rated = ObjectRating.objects.filter(user=user, bundle=bundle).exists()
    if is_already_rated:
        ObjectRating.objects.filter(user=user, bundle=bundle).update(**data)
    else:
        ObjectRating.objects.create(bundle=bundle,
                                    user=user,
                                    **data)

    return bundle
