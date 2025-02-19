from django.db import models

from apps.utils.enums import TimeZones
from apps.utils.models import DeletedMixin, TimestampMixin


def upload_shop_image(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'shop_image', filename)


# Create your models here.
class Country(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=36)


class City(DeletedMixin, TimestampMixin):
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=255)
    time_zone = models.CharField(max_length=8, choices=TimeZones, default="+5")


class ShopCategory(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)


class Shop(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    blocked = models.BooleanField(default=False)
    open_from = models.TimeField(null=True)
    open_until = models.TimeField(null=True)
    image = models.ImageField(upload_to=upload_shop_image, null=True, blank=True)
    rating = models.FloatField(null=True, default=0)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    two_gis_link = models.CharField(max_length=255, null=True)
    contacts = models.TextField(null=True)
    city = models.ForeignKey(to=City, null=True, on_delete=models.CASCADE, related_name='shops')
    category = models.ForeignKey(to=ShopCategory, null=True, on_delete=models.CASCADE, related_name='shops')
    # schedule = models.OneToOneField(to='shops.ShopSchedule', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Заведение: {self.name}"
