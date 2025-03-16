from django.db import models

from apps.activities.models import Course, Event
from apps.services.models import ServiceProvider
from apps.shops.bundles.models import Bundle
from apps.shops.models import Shop
from apps.shops.products.models import Product
from apps.users.models import User
from apps.utils.enums import ObjectRatingStatus
from apps.utils.models import DeletedMixin, TimestampMixin


# Create your models here.
class ObjectRating(DeletedMixin, TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    rating = models.PositiveSmallIntegerField()
    review = models.CharField(max_length=255, null=True)
    status = models.CharField(choices=ObjectRatingStatus.choices, default=ObjectRatingStatus.ON_MODERATION)
