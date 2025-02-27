from rest_framework.generics import get_object_or_404

from apps.shops.commodity_groups.models import CommodityGroupCategory, CommodityGroup
from apps.shops.products.models import Product


def add_commodity_group_category(data):
    commodity_group_category = CommodityGroupCategory.objects.create(**data)
    return commodity_group_category


def update_commodity_group_category(pk, data):
    commodity_group_category = get_object_or_404(CommodityGroupCategory, pk=pk)

    for key, value in data.items():
        setattr(commodity_group_category, key, value)

    commodity_group_category.save()
    return commodity_group_category


def delete_commodity_group_category(pk):
    commodity_group_category = get_object_or_404(CommodityGroupCategory, pk=pk)
    commodity_group_category.deleted = True
    commodity_group_category.save(update_fields=['deleted'])


def add_commodity_group(data):
    products = data.pop('products', [])
    commodity_group = CommodityGroup.objects.create(**data)
    Product.objects.filter(id__in=products).update(commodity_group=commodity_group)

    return commodity_group


def update_commodity_group(pk, data):
    products = data.pop('products', [])
    commodity_group = get_object_or_404(CommodityGroup, pk=pk)

    for key, value in data.items():
        setattr(commodity_group, key, value)
    Product.objects.filter(id__in=products).update(commodity_group=commodity_group)
    commodity_group.save()
    return commodity_group


def delete_commodity_group(pk):
    commodity_group = get_object_or_404(CommodityGroup, pk=pk)
    commodity_group.deleted = True
    commodity_group.save(update_fields=['deleted'])
