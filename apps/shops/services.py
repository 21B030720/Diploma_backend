from rest_framework.generics import get_object_or_404

from apps.shops.models import Shop, City, Country


def add_country(data):
    country = Country.objects.create(**data)
    return country


def update_country(pk, data):
    country = get_object_or_404(Country, pk=pk)

    for key, value in data.items():
        setattr(country, key, value)

    country.save()
    return country


def delete_country(pk):
    country = get_object_or_404(Country, pk=pk)
    country.deleted = True
    country.save()


def add_city(data):
    city = City.objects.create(**data)
    return city


def update_city(pk, data):
    city = get_object_or_404(City, pk=pk)
    for key, value in data.items():
        setattr(city, key, value)

    city.save()
    return city


def delete_city(pk):
    city = City.objects.get(pk=pk)
    city.deleted = True
    city.save(update_fields=['deleted'])


def add_shop(data):
    shop = Shop.objects.create(**data)
    return shop


