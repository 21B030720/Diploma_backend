from django.db import models
from django.db.models import Sum, Avg

from apps.shops.models import Shop
from apps.shops.products.models import Product
from apps.utils.models import DeletedMixin, TimestampMixin


# Create your models here.
class Bundle(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='bundles')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='bundles')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def avg_rating(self):
        avg_rating = self.ratings.aggregate(avg_rating=Avg('rating'))
        return avg_rating['avg_rating']

    @property
    def rating_count(self):
        rating_count = self.ratings.count()
        return rating_count
