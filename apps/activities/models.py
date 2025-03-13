from django.db import models

from apps.utils.enums import CoursePaymentPeriod
from apps.utils.models import DeletedMixin, TimestampMixin


def upload_event_image(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'event_image', filename)


def upload_course_image(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'course_image', filename)


# Create your models here.
class EventCategory(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Event(DeletedMixin, TimestampMixin):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='events')
    image = models.ImageField(upload_to=upload_event_image, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tickets_left = models.PositiveIntegerField(default=0)
    organizator = models.CharField(max_length=255)
    contacts = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    two_gis_link = models.URLField(null=True, blank=True)
    date_held = models.DateTimeField(null=True, blank=True)
    from_age = models.PositiveIntegerField(null=True, blank=True)
    to_age = models.PositiveIntegerField(null=True, blank=True)


class CourseCategory(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Course(DeletedMixin, TimestampMixin):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses', null=True)
    image = models.ImageField(upload_to=upload_event_image, null=True, blank=True)
    description = models.TextField()
    company = models.CharField(max_length=255)
    contacts = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    two_gis_link = models.URLField(null=True, blank=True)
    from_age = models.PositiveIntegerField(null=True, blank=True)
    to_age = models.PositiveIntegerField(null=True, blank=True)


class CoursePriceList(DeletedMixin, TimestampMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_period = models.CharField(choices=CoursePaymentPeriod.choices, max_length=255, default=CoursePaymentPeriod.MONTHLY)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_prices')
