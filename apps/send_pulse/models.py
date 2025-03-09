from django.db import models

from apps.users.models import User
from apps.utils.models import DeletedMixin, TimestampMixin


# Create your models here.
class UserCode(DeletedMixin, TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='code')
    code = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(default=False)
