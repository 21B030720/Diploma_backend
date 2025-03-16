from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.reviews.serializers import ObjectRatingSerializer, RateSerializer
from apps.shops.bundles.filters import BundleFilterSet
from apps.shops.bundles.models import Bundle
from apps.shops.bundles.serializers import BundleSerializer, BundleCreateSerializer
from apps.shops.bundles.services import add_bundle, update_bundle, delete_bundle, rate_bundle
from apps.shops.products.serializers import ProductSerializer
from apps.users.permissions import IsAdmin, IsManager, ReadOnly, IsClientUser
from apps.utils.enums import RoleType
from apps.utils.filters import SortingFilterBackend
from apps.utils.swagger_params import shop_id_param, sort_param
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.
@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      tags=['bundles'],
                      manual_parameters=[
                          shop_id_param,
                          sort_param
                      ]
                  ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['bundles']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['bundles']))
class BundleViewSet(BaseViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet
                    ):
    queryset = Bundle.objects.select_related(
        'shop'
    ).prefetch_related(
        'products'
    )
    serializer_class = BundleSerializer
    parser_classes = (JSONParser, )
    serializers = {
        'create': BundleCreateSerializer,
        'update': BundleCreateSerializer,
        'products': ProductSerializer,
        'rate_bundle': RateSerializer,
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = BundleFilterSet
    permission_classes = [IsAdmin | IsManager | ReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user
        if user.is_authenticated:
            context['user'] = user
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'crm_user'):
            if user.crm_user.role == RoleType.ADMIN:
                pass
            elif user.crm_user.role == RoleType.MANAGER:
                queryset = queryset.filter(shop_id=user.crm_user.shop_id)

        shop_ids = self.request.query_params.getlist('shop_id', [])
        if shop_ids:
            queryset = queryset.filter(shop_id__in=shop_ids)

        return queryset

    def perform_create(self, serializer):
        product = add_bundle(serializer.validated_data)
        return product

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        category = update_bundle(pk, serializer.validated_data)
        return category

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_bundle(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(tags=['bundles'],
                                                    request_body=BundleCreateSerializer,
                                                    responses={
                                                        201: BundleSerializer(),
                                                    }))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        serializer = BundleSerializer(obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(tags=['bundles'],
                                                    request_body=BundleCreateSerializer,
                                                    responses={
                                                        201: BundleSerializer(),
                                                    }))
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer = BundleSerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='products',
                      decorator=swagger_auto_schema(
                          tags=['bundles'],
                          responses={
                              200: BundleSerializer(many=True),
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='products')
    def products(self, request, *args, **kwargs):
        instance = self.get_object()
        products = instance.products.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(name='rate_bundle',
                      decorator=swagger_auto_schema(
                          tags=['bundles'],
                          responses={
                              201: BundleSerializer()
                          }
                      ))
    @action(methods=['POST'], detail=True, url_path='rate-bundle', permission_classes=[IsClientUser])
    def rate_bundle(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.get_object()
        user = self.request.user
        service_provider = rate_bundle(obj, user, serializer.validated_data)
        serializer = BundleSerializer(service_provider, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(name='bundle_reviews',
                      decorator=swagger_auto_schema(
                          tags=['bundles'],
                          responses={
                              200: ObjectRatingSerializer(many=True)
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='bundle-reviews')
    def bundle_reviews(self, request, *args, **kwargs):
        obj = self.get_object()
        reviews = obj.ratings.filter(
            review__isnull=False
        )
        if self.request.user.is_authenticated:
            reviews = reviews.exclude(
                user=self.request.user
            )
        reviews = reviews.order_by('-changed_at')
        serializer = ObjectRatingSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(name='my_review',
                      decorator=swagger_auto_schema(
                          tags=['bundles'],
                          responses={
                              200: ObjectRatingSerializer()
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='my-review', permission_classes=[IsClientUser])
    def my_review(self, request, *args, **kwargs):
        obj = self.get_object()
        review = obj.ratings.filter(user=self.request.user).first()
        serializer = ObjectRatingSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
