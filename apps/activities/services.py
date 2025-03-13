from django.db import transaction
from rest_framework.generics import get_object_or_404

from apps.activities.models import EventCategory, Event, CourseCategory, Course, CoursePriceList


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


def add_course_category(data):
    course_category = CourseCategory.objects.create(**data)
    return course_category


def update_course_category(pk, data):
    course_category = get_object_or_404(CourseCategory, pk=pk)

    for key, value in data.items():
        setattr(course_category, key, value)

    course_category.save()
    return course_category


def delete_course_category(pk):
    course_category = get_object_or_404(CourseCategory, pk=pk)
    course_category.deleted = True
    course_category.save(update_fields=['deleted'])


@transaction.atomic
def add_course(data):
    course_prices = data.pop('course_prices', [])

    course = Course.objects.create(**data)

    course_prices_list = []

    for course_price in course_prices:
        course_price_obj = CoursePriceList(**course_price, course=course)
        course_prices_list.append(course_price_obj)

    CoursePriceList.objects.bulk_create(course_prices_list)

    return course


@transaction.atomic
def update_course(pk, data):
    course = get_object_or_404(Course, pk=pk)
    _course_prices = data.pop('course_prices', [])

    for key, value in data.items():
        setattr(course, key, value)

    update_course_price_list(course, _course_prices)

    course.save()


def update_course_price_list(course, course_prices):
    if not course_prices:
        return

    course_price_ids = []
    for course_price in course_prices:
        if course_price.get('id'):
            course_price_ids.append(course_price.get('id'))

    CoursePriceList.objects.filter(
        course=course,
    ).exclude(id__in=course_price_ids).delete()

    for course_price in course_prices:
        if course_price.get('id'):
            course_price_id = course_price.pop('id')
            CoursePriceList.objects.filter(pk=course_price_id).update(**course_price)
        else:
            CoursePriceList.objects.create(course=course, **course_price)


def delete_course(pk):
    course = get_object_or_404(Course, pk=pk)
    course.course_prices.update(deleted=True)
    course.deleted = True
    course.save(update_fields=['deleted'])
