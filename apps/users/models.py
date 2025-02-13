from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps import shops
from apps.utils.enums import RoleType
from apps.utils.models import DeletedMixin, TimestampMixin


# Create your models here.
class User(DeletedMixin, AbstractBaseUser, PermissionsMixin, TimestampMixin):
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return self.username if self.username else self.pk


class CRMUser(DeletedMixin, TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='crm_user')
    name = models.CharField(max_length=255, blank=True)
    phone_number = PhoneNumberField(blank=True)
    role = models.CharField(choices=RoleType.choices, max_length=255)
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, related_name='users', null=True)
