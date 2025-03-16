from django.db import models
from django.db.models import Avg
from phonenumber_field.modelfields import PhoneNumberField

from apps.users.models import User
from apps.utils.enums import ServiceType, ServicePaymentPeriod
from apps.utils.models import DeletedMixin, TimestampMixin


def upload_service_category_icon(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'service_category_icon', filename)


def upload_service_resume(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'service_resume', filename)


def upload_service_personal_information_profile_photo(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'service_profile_photo', filename)


# Create your models here.
class ServiceCategory(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to=upload_service_category_icon, null=True, blank=True)


class ServiceProvider(DeletedMixin, TimestampMixin):
    full_name = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to=upload_service_personal_information_profile_photo, null=True, blank=True)
    phone_number = PhoneNumberField()
    email = models.EmailField(null=True, blank=True)
    social_networks = models.CharField(max_length=255, null=True, blank=True)
    resume = models.FileField(upload_to=upload_service_resume, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def avg_rating(self):
        avg_rating = self.ratings.aggregate(avg_rating=Avg('rating'))
        return avg_rating['avg_rating']

    @property
    def rating_count(self):
        rating_count = self.ratings.count()
        return rating_count


class Service(DeletedMixin, TimestampMixin):
    title = models.CharField(max_length=255)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(choices=ServiceType.choices)
    details = models.TextField()
    address = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_period = models.CharField(choices=ServicePaymentPeriod.choices,
                                      default=ServicePaymentPeriod.HOURLY)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
