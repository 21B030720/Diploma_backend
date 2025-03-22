from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.reviews.serializers import ObjectRatingSerializer, RateSerializer
from apps.shops.products.filters import ProductCategoryFilterSet, ProductFilterSet
from apps.shops.products.models import ProductCategory, Product
from apps.shops.products.serializers import ProductCategorySerializer, ProductCategoryCreateSerializer, \
    ProductCategorySimpleSerializer, ProductSerializer, ProductSimpleSerializer, ProductCreateSerializer
from apps.shops.products.services import add_product_category, update_product_category, delete_product_category, \
    add_product, delete_product, update_product, rate_product
from apps.users.permissions import IsAdmin, IsManager, ReadOnly, IsClientUser
from apps.utils.enums import RoleType
from apps.utils.filters import SortingFilterBackend
from apps.utils.swagger_params import shop_id_param, sort_param, category_name_param, from_age_param, to_age_param
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.
@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      tags=['products-categories'],
                      manual_parameters=[
                          shop_id_param,
                          sort_param
                      ]
                  ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['products-categories']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['products-categories']))
class ProductCategoryViewSet(BaseViewSet,
                             mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             GenericViewSet
                             ):
    queryset = ProductCategory.objects.select_related(
        'shop'
    )
    serializer_class = ProductCategorySerializer
    parser_classes = (DrfNestedParser,)
    serializers = {
        'create': ProductCategoryCreateSerializer,
        'update': ProductCategoryCreateSerializer,
        'all': ProductCategorySimpleSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = ProductCategoryFilterSet
    permission_classes = [IsAdmin | IsManager | ReadOnly]

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
        category = add_product_category(serializer.validated_data)
        return category

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        category = update_product_category(pk, serializer.validated_data)
        return category

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_product_category(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(tags=['products-categories'],
                                                    request_body=ProductCategoryCreateSerializer,
                                                    responses={
                                                        201: ProductCategorySerializer(),
                                                    }))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = ProductCategorySerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(tags=['products-categories'],
                                                    request_body=ProductCategoryCreateSerializer,
                                                    responses={
                                                        201: ProductCategorySerializer(),
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

        serializer = ProductCategorySerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['products-categories'],
                                                                responses={
                                                                    200: ProductCategorySimpleSerializer(many=True)
                                                                }))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      tags=['products'],
                      manual_parameters=[
                          shop_id_param,
                          sort_param,
                          category_name_param,
                          from_age_param,
                          to_age_param
                      ]
                  ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['products']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['products']))
class ProductViewSet(BaseViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet
                     ):
    queryset = Product.objects.select_related(
        'shop'
    )
    serializer_class = ProductSerializer
    parser_classes = (DrfNestedParser, JSONParser)
    serializers = {
        'create': ProductCreateSerializer,
        'update': ProductCreateSerializer,
        'all': ProductSimpleSerializer,
        'rate_product': RateSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = ProductFilterSet
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

        category_names = self.request.query_params.getlist('category_name', [])
        if category_names:
            queryset = queryset.filter(category__name__in=category_names)

        shop_ids = self.request.query_params.getlist('shop_id', [])
        if shop_ids:
            queryset = queryset.filter(shop_id__in=shop_ids)

        return queryset

    def perform_create(self, serializer):
        product = add_product(serializer.validated_data)
        return product

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        category = update_product(pk, serializer.validated_data)
        return category

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_product(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(tags=['products'],
                                                    request_body=ProductCreateSerializer,
                                                    responses={
                                                        201: ProductSerializer(),
                                                    }))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        serializer = ProductSerializer(obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(tags=['products'],
                                                    request_body=ProductCreateSerializer,
                                                    responses={
                                                        201: ProductSerializer(),
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

        serializer = ProductSerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['products'],
                                                                responses={
                                                                    200: ProductSimpleSerializer(many=True)
                                                                }))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @method_decorator(name='rate_product',
                      decorator=swagger_auto_schema(
                          tags=['products'],
                          responses={
                              201: ProductSerializer()
                          }
                      ))
    @action(methods=['POST'], detail=True, url_path='rate-product', permission_classes=[IsClientUser], parser_classes=(JSONParser, ))
    def rate_product(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.get_object()
        user = self.request.user
        service_provider = rate_product(obj, user, serializer.validated_data)
        serializer = ProductSerializer(service_provider, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(name='product_reviews',
                      decorator=swagger_auto_schema(
                          tags=['products'],
                          responses={
                              200: ObjectRatingSerializer(many=True)
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='product-reviews')
    def product_reviews(self, request, *args, **kwargs):
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
                          tags=['products'],
                          responses={
                              200: ObjectRatingSerializer()
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='my-review')
    def my_review(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return Response({'details': 'You must be logged in to see your review.'}, status=status.HTTP_403_FORBIDDEN)
        obj = self.get_object()
        review = obj.ratings.filter(user=self.request.user).first()
        serializer = ObjectRatingSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
