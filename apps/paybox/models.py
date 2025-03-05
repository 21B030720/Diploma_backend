from django.db import models

from apps.users.models import User
from apps.utils.models import DeletedMixin, TimestampMixin


class Card(DeletedMixin, TimestampMixin):
    card_hash = models.CharField(max_length=19)
    card_month = models.CharField(max_length=2)
    card_year = models.CharField(max_length=4)
    bank = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    card_3ds = models.BooleanField()
    status = models.CharField(max_length=255)
    card_id = models.IntegerField()
    card_token = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    default = models.BooleanField(default=False)