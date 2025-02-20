from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.shops.products.models import ProductCategory
from apps.shops.products.serializers import ProductCategorySerializer, ProductCategoryCreateSerializer, \
    ProductCategorySimpleSerializer
from apps.shops.products.services import add_product_category, update_product_category, delete_product_category
from apps.users.permissions import IsAdminOrReadOnly, IsManagerOrReadOnly
from apps.utils.enums import RoleType
from apps.utils.filters import SortingFilterBackend
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        tags=['products-categories']
    )
)
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
    parser_classes = (DrfNestedParser, )
    serializers = {
        'create': ProductCategoryCreateSerializer,
        'update': ProductCategoryCreateSerializer,
        'all': ProductCategorySimpleSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    permission_classes = [IsAdminOrReadOnly | IsManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.crm_user.role == RoleType.ADMIN:
            pass
        elif user.crm_user.role == RoleType.MANAGER:
            queryset = queryset.filter(shop_id=user.crm_user.shop_id)

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
                                                        200: ProductCategorySerializer(),
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
                                                        200: ProductCategorySerializer(),
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
