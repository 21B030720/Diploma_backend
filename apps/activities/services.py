from rest_framework.generics import get_object_or_404

from apps.activities.models import EventCategory, Event


def add_event_category(data):
    event_category = EventCategory.objects.create(**data)
    return event_category


def update_event_category(pk, data):
    event_category = get_object_or_404(EventCategory, pk=pk)

    for key, value in data.items():
        setattr(event_category, key, value)

    event_category.save()
    return event_category


def delete_event_category(pk):
    event_category = get_object_or_404(EventCategory, pk=pk)
    event_category.deleted = True
    event_category.save(update_fields=['deleted'])


def add_event(data):
    event = Event.objects.create(**data)
    return event


def update_event(pk, data):
    event = get_object_or_404(Event, pk=pk)

    for key, value in data.items():
        setattr(event, key, value)

    event.save()
    return event


def delete_event(pk):
    event = get_object_or_404(Event, pk=pk)
    event.deleted = True
    event.save(update_fields=['deleted'])
