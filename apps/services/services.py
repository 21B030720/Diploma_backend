from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from apps.reviews.models import ObjectRating
from apps.services.models import ServiceCategory, ServiceProvider, Service


def add_service_category(data):
    service_category = ServiceCategory.objects.create(**data)
    return service_category


def update_service_category(pk, data):
    service_category = get_object_or_404(ServiceCategory, pk=pk)

    for key, value in data.items():
        setattr(service_category, key, value)

    service_category.save()
    return service_category


def delete_service_category(pk):
    service_category = get_object_or_404(ServiceCategory, pk=pk)
    service_category.deleted = True
    service_category.save(update_fields=['deleted'])


def add_service(data):
    service_provider_data = data.pop('service_provider')
    service_provider = ServiceProvider.objects.create(**service_provider_data)
    service = Service.objects.create(**data, service_provider=service_provider)
    return service


def update_service(pk, data):
    service_provider_data = data.pop('service_provider')
    service = get_object_or_404(Service, pk=pk)
    service_provider = service.service_provider

    for key, value in service_provider_data.items():
        setattr(service_provider, key, value)
    service_provider.save()

    for key, value in data.items():
        setattr(service, key, value)
    service.save()

    return service


def delete_service(pk):
    service = get_object_or_404(Service, pk=pk)
    service.deleted = True
    service.save(update_fields=['deleted'])


def rate_service_provider(service, user, data):
    service_provider = service.service_provider
    if not service_provider:
        raise ValidationError("This service does not have a provider.")

    is_already_rated = ObjectRating.objects.filter(user=user, service_provider=service_provider).exists()
    if is_already_rated:
        ObjectRating.objects.filter(user=user, service_provider=service_provider).update(**data)
    else:
        ObjectRating.objects.create(service_provider=service_provider,
                                    user=user,
                                    **data)

    return service_provider
