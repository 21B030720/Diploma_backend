from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.activities.filters import EventCategoryFilterSet, EventFilterSet, CourseCategoryFilterSet, CourseFilterSet
from apps.activities.models import EventCategory, Event, CourseCategory, Course
from apps.activities.serializers import EventCategorySerializer, EventCategoryCreateSerializer, EventSerializer, \
    EventCreateSerializer, CourseCategorySerializer, CourseCategoryCreateSerializer, CourseSerializer, \
    CourseCreateSerializer
from apps.activities.services import delete_event_category, add_event_category, update_event_category, add_event, \
    update_event, delete_event, add_course_category, update_course_category, delete_course_category, add_course, \
    update_course, delete_course
from apps.users.permissions import IsAdmin, ReadOnly
from apps.utils.filters import SortingFilterBackend
from apps.utils.swagger_params import from_age_param, to_age_param
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
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    serializers = {
        'create': EventCategoryCreateSerializer,
        'update': EventCategoryCreateSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = EventCategoryFilterSet
    sorting_fields = {
    }
    permission_classes = [IsAdmin | ReadOnly]

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
                              201: EventCategorySerializer()
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
                              201: EventCategorySerializer()
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


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      tags=['events'],
                      manual_parameters=[
                          from_age_param,
                          to_age_param
                      ]
                  ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['events']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['events']))
class EventViewSet(BaseViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    serializers = {
        'create': EventCreateSerializer,
        'update': EventCreateSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = EventFilterSet
    sorting_fields = {
    }
    parser_classes = (DrfNestedParser, )
    permission_classes = [IsAdmin | ReadOnly]

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
                          tags=['events'],
                          responses={
                              201: EventSerializer()
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
                          tags=['events'],
                          responses={
                              201: EventSerializer()
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

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['events']))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['course-categories']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['course-categories']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['course-categories']))
class CourseCategoryViewSet(BaseViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            GenericViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    serializers = {
        'create': CourseCategoryCreateSerializer,
        'update': CourseCategoryCreateSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = CourseCategoryFilterSet
    sorting_fields = {
    }
    permission_classes = [IsAdmin | ReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def perform_create(self, serializer):
        course_category = add_course_category(serializer.validated_data)
        return course_category

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        course_category = update_course_category(pk, serializer.validated_data)
        return course_category

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_course_category(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(
                          tags=['course-categories'],
                          responses={
                              201: CourseCategorySerializer()
                          }
                      ))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = CourseCategorySerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(
                          tags=['course-categories'],
                          responses={
                              201: CourseCategorySerializer()
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

        serializer = CourseCategorySerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['course-categories']))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['courses']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['courses']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['courses']))
class CourseViewSet(BaseViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    serializers = {
        'create': CourseCreateSerializer,
        'update': CourseCreateSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = CourseFilterSet
    sorting_fields = {
    }
    parser_classes = (DrfNestedParser, JSONParser)
    permission_classes = [IsAdmin | ReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def perform_create(self, serializer):
        course = add_course(serializer.validated_data)
        return course

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        course = update_course(pk, serializer.validated_data)
        return course

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_course(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(
                          tags=['courses'],
                          responses={
                              201: CourseSerializer()
                          }
                      ))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = CourseSerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(
                          tags=['courses'],
                          responses={
                              201: CourseSerializer()
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

        serializer = CourseSerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['courses']))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
