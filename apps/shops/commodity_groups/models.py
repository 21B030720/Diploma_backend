from django.db import models

from apps.shops.models import Shop
from apps.utils.models import DeletedMixin, TimestampMixin


def upload_commodity_group_category_icon(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'commodity_group_category_icon', filename)


def upload_commodity_group_image(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'commodity_group_image', filename)


# Create your models here.
class CommodityGroupCategory(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to=upload_commodity_group_category_icon)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='commodity_group_categories')


class CommodityGroup(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_commodity_group_image)
    description = models.TextField()
    category = models.ForeignKey(CommodityGroupCategory, on_delete=models.CASCADE, related_name='commodity_groups')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='commodity_groups')
