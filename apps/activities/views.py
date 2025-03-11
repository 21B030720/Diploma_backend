from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.activities.models import EventCategory, Event
from apps.activities.serializers import EventCategorySerializer, EventCategoryCreateSerializer, EventSerializer, \
    EventCreateSerializer
from apps.activities.services import delete_event_category, add_event_category, update_event_category, add_event, \
    update_event, delete_event
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.
@method_decorator(name='list', decorator=swagger_auto_schema(tags=['event-categories']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['event-categories']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['event-categories']))
class EventCategoryViewSet(BaseViewSet,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericViewSet):
    serializer_class = EventCategorySerializer
    serializers = {
        'create': EventCategoryCreateSerializer,
        'update': EventCategoryCreateSerializer
    }
    queryset = EventCategory.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def perform_create(self, serializer):
        event_category = add_event_category(serializer.validated_data)
        return event_category

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        event_category = update_event_category(pk, serializer.validated_data)
        return event_category

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_event_category(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(
                          tags=['event-categories'],
                          responses={
                              200: EventCategorySerializer()
                          }
                      ))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = EventCategorySerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(
                          tags=['event-categories'],
                          responses={
                              200: EventCategorySerializer()
                          }
                      ))
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer = EventCategorySerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['event-categories']))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['event']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['event']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['event']))
class EventViewSet(BaseViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = EventSerializer
    serializers = {
        'create': EventCreateSerializer,
        'update': EventCreateSerializer
    }
    queryset = Event.objects.all()
    parser_classes = (DrfNestedParser, )

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def perform_create(self, serializer):
        event = add_event(serializer.validated_data)
        return event

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        event = update_event(pk, serializer.validated_data)
        return event

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_event(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(
                          tags=['event'],
                          responses={
                              200: EventSerializer()
                          }
                      ))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = EventSerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(
                          tags=['event'],
                          responses={
                              200: EventSerializer()
                          }
                      ))
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer = EventSerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['event']))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
