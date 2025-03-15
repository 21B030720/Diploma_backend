from django.db.models import TextChoices


class RoleType(TextChoices):
    ADMIN = 'admin', 'admin'
    MANAGER = 'manager', 'manager'


TimeZones = [
    ('-12', 'GMT-12'),
    ('-11', 'GMT-11'),
    ('-10', 'GMT-10'),
    ('-9', 'GMT-9'),
    ('-8', 'GMT-8'),
    ('-7', 'GMT-7'),
    ('-6', 'GMT-6'),
    ('-5', 'GMT-5'),
    ('-4', 'GMT-4'),
    ('-3', 'GMT-3'),
    ('-2', 'GMT-2'),
    ('-1', 'GMT-1'),
    ('+0', 'GMT+0'),
    ('+1', 'GMT+1'),
    ('+2', 'GMT+2'),
    ('+3', 'GMT+3'),
    ('+4', 'GMT+4'),
    ('+5', 'GMT+5'),
    ('+6', 'GMT+6'),
    ('+7', 'GMT+7'),
    ('+8', 'GMT+8'),
    ('+9', 'GMT+9'),
    ('+10', 'GMT+10'),
    ('+11', 'GMT+11'),
    ('+12', 'GMT+12'),
    ('+13', 'GMT+13'),
    ('+14', 'GMT+14'),
]


class Measures(TextChoices):
    WEIGHT = 'KG', 'KG'
    LITER = 'L', 'L'
    PIECE = 'PC', 'PC'


class TransactionType(TextChoices):
    DEPOSIT = 'deposit', 'deposit'


class TransactionStatus(TextChoices):
    FINISHED = 'finished', 'finished'
    PENDING = 'pending', 'pending'
    CANCELED = 'canceled', 'canceled'


class CoursePaymentPeriod(TextChoices):
    MONTHLY = 'monthly', 'monthly'
    WEEKLY = 'weekly', 'weekly'
    DAILY = 'daily', 'daily'
    HOURLY = 'hourly', 'hourly'


class ServiceType(TextChoices):
    ONLINE = 'online', 'online'
    OFFLINE = 'offline', 'offline'
    HYBRID = 'hybrid', 'hybrid'


class ServicePaymentPeriod(TextChoices):
    MONTHLY = 'monthly', 'monthly'
    WEEKLY = 'weekly', 'weekly'
    DAILY = 'daily', 'daily'
    HOURLY = 'hourly', 'hourly'


class ItemType(TextChoices):
    PRODUCT = 'PRODUCT', 'PRODUCT'
    BUNDLE = 'BUNDLE', 'BUNDLE'


class OrderStatus(TextChoices):
    WAITING = 'WAITING', 'WAITING'
    PARTIALLY_GIVEN = 'PARTIALLY_GIVEN', 'PARTIALLY_GIVEN'
    TOTALLY_GIVEN = 'TOTALLY_GIVEN', 'TOTALLY_GIVEN'
    CANCELLED = 'CANCELLED', 'CANCELLED'


class OrderItemStatus(TextChoices):
    WAITING_FOR_COURIER = 'WAITING_FOR_COURIER', 'WAITING_FOR_COURIER'
    GIVEN_TO_COURIER = 'GIVEN_TO_COURIER', 'GIVEN_TO_COURIER'
    GIVEN_TO_CUSTOMER = 'GIVEN_TO_CUSTOMER', 'GIVEN_TO_CUSTOMER'
    CANCELLED = 'CANCELLED', 'CANCELLED'