from django.db import models

from apps.shops.models import Shop
from apps.shops.products.models import Product
from apps.utils.models import DeletedMixin, TimestampMixin


# Create your models here.
class Bundle(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='bundles')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='bundles')
