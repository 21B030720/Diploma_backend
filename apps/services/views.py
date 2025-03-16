from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.reviews.serializers import RateSerializer, ObjectRatingSerializer
from apps.services.filters import ServiceCategoryFilterSet, ServiceFilterSet
from apps.services.models import ServiceCategory, Service
from apps.services.serializers import ServiceCategorySerializer, ServiceCategoryCreateSerializer, ServiceSerializer, \
    ServiceCreateSerializer, ServiceProviderSerializer
from apps.services.services import add_service_category, update_service_category, delete_service_category, add_service, \
    update_service, delete_service, rate_service_provider
from apps.users.permissions import IsClientUser, IsAdmin, ReadOnly
from apps.utils.filters import SortingFilterBackend
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.
@method_decorator(name='list', decorator=swagger_auto_schema(tags=['service-categories']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['service-categories']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['service-categories']))
class ServiceCategoryViewSet(BaseViewSet,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             GenericViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    serializers = {
        'create': ServiceCategoryCreateSerializer,
        'update': ServiceCategoryCreateSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = ServiceCategoryFilterSet
    sorting_fields = {
    }
    parser_classes = (DrfNestedParser,)
    permission_classes = [IsAdmin | ReadOnly]

    def perform_create(self, serializer):
        event_category = add_service_category(serializer.validated_data)
        return event_category

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        event_category = update_service_category(pk, serializer.validated_data)
        return event_category

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_service_category(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(
                          tags=['service-categories'],
                          responses={
                              201: ServiceCategorySerializer()
                          }
                      ))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = ServiceCategorySerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(
                          tags=['service-categories'],
                          responses={
                              201: ServiceCategorySerializer()
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

        serializer = ServiceCategorySerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['service-categories']))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      tags=['service'],


                  ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['service']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['service']))
class ServiceViewSet(BaseViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    serializers = {
        'create': ServiceCreateSerializer,
        'update': ServiceCreateSerializer,
        'rate_provider': RateSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = ServiceFilterSet
    sorting_fields = {

    }
    parser_classes = (DrfNestedParser, JSONParser)
    permission_classes = [IsAdmin | ReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user
        if user.is_authenticated:
            context['user'] = user
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        category_ids = self.request.query_params.getlist('category_id', [])
        if category_ids:
            queryset = queryset.filter(category_id__in=category_ids)

        return queryset

    def perform_create(self, serializer):
        event_category = add_service(serializer.validated_data)
        return event_category

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        event_category = update_service(pk, serializer.validated_data)
        return event_category

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_service(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(
                          tags=['service'],
                          responses={
                              201: ServiceSerializer()
                          }
                      ))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = ServiceSerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(
                          tags=['service'],
                          responses={
                              201: ServiceSerializer()
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

        serializer = ServiceSerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['service']))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @method_decorator(name='rate_provider',
                      decorator=swagger_auto_schema(
                          tags=['service'],
                          responses={
                              201: ServiceProviderSerializer()
                          }
                      ))
    @action(methods=['POST'], detail=True, url_path='rate-provider', permission_classes=[IsClientUser])
    def rate_provider(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.get_object()
        user = self.request.user
        service_provider = rate_service_provider(obj, user, serializer.validated_data)
        serializer = ServiceProviderSerializer(service_provider, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(name='provider_reviews',
                      decorator=swagger_auto_schema(
                          tags=['service'],
                          responses={
                              200: ObjectRatingSerializer(many=True)
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='provider-reviews')
    def provider_reviews(self, request, *args, **kwargs):
        obj = self.get_object()
        service_provider = obj.service_provider
        reviews = service_provider.ratings.filter(
            review__isnull=False
        ).exclude(
            user=self.request.user
        ).order_by('-changed_at')
        serializer = ObjectRatingSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(name='my_review',
                      decorator=swagger_auto_schema(
                          tags=['service'],
                          responses={
                              200: ObjectRatingSerializer()
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='my-review', permission_classes=[IsClientUser])
    def my_review(self, request, *args, **kwargs):
        obj = self.get_object()
        service_provider = obj.service_provider
        review = service_provider.ratings.filter(user=self.request.user).first()
        serializer = ObjectRatingSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
