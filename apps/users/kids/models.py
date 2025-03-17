from django.db import models
from django.db.models import Sum

from apps.users.models import ClientUser
from apps.utils.enums import OrderItemStatus
from apps.utils.models import DeletedMixin, TimestampMixin


def upload_kid_image(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'kid_image', filename)


def upload_kid_level_image(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'kid_level_image', filename)


# Create your models here.
class KidLevel(DeletedMixin, TimestampMixin):
    level_name = models.CharField(max_length=255)
    level_image = models.ImageField(upload_to=upload_kid_level_image, null=True, blank=True)
    level_position = models.PositiveSmallIntegerField(unique=True)
    from_xp = models.DecimalField(max_digits=10, decimal_places=2)
    to_xp = models.DecimalField(max_digits=10, decimal_places=2)


class Kid(DeletedMixin, TimestampMixin):
    client_user = models.ForeignKey(ClientUser, related_name='kids', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_kid_image, null=True, blank=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    details = models.TextField(default='', blank=True)
    kid_level = models.ForeignKey(KidLevel, related_name='kids', on_delete=models.CASCADE, blank=True)

    @property
    def xp(self):
        order_items = self.order_items.exclude(status=OrderItemStatus.CANCELLED)
        total_price = order_items.aggregate(total=Sum('final_price'))['total']
        if total_price:
            return total_price
        return 0
