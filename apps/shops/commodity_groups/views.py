from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from apps.shops.commodity_groups.filters import CommodityGroupCategoryFilterSet, CommodityGroupFilterSet
from apps.shops.commodity_groups.models import CommodityGroupCategory, CommodityGroup
from apps.shops.commodity_groups.serializers import CommodityGroupCategorySerializer, \
    CommodityGroupCategoryCreateSerializer, CommodityGroupCategorySimpleSerializer, CommodityGroupSerializer, \
    CommodityGroupCreateSerializer
from apps.shops.commodity_groups.services import add_commodity_group_category, update_commodity_group_category, \
    delete_commodity_group_category, update_commodity_group, add_commodity_group, delete_commodity_group
from apps.shops.products.serializers import ProductSerializer
from apps.users.permissions import IsAdminOrReadOnly, IsManagerOrReadOnly
from apps.utils.enums import RoleType
from apps.utils.filters import SortingFilterBackend
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        tags=['commodity-groups-categories']
    )
)
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['commodity-groups-categories']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['commodity-groups-categories']))
class CommodityGroupCategoryViewSet(BaseViewSet,
                                    mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    GenericViewSet
                                    ):
    queryset = CommodityGroupCategory.objects.select_related(
        'shop'
    )
    serializer_class = CommodityGroupCategorySerializer
    parser_classes = (DrfNestedParser,)
    serializers = {
        'create': CommodityGroupCategoryCreateSerializer,
        'update': CommodityGroupCategoryCreateSerializer,
        'all': CommodityGroupCategorySimpleSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = CommodityGroupCategoryFilterSet
    permission_classes = [IsAdminOrReadOnly | IsManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'crm_user'):
            if user.crm_user.role == RoleType.ADMIN:
                pass
            elif user.crm_user.role == RoleType.MANAGER:
                queryset = queryset.filter(shop_id=user.crm_user.shop_id)

        return queryset

    def perform_create(self, serializer):
        category = add_commodity_group_category(serializer.validated_data)
        return category

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        category = update_commodity_group_category(pk, serializer.validated_data)
        return category

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_commodity_group_category(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(tags=['commodity-groups-categories'],
                                                    request_body=CommodityGroupCategoryCreateSerializer,
                                                    responses={
                                                        200: CommodityGroupCategorySerializer(),
                                                    }))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = CommodityGroupCategorySerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(tags=['commodity-groups-categories'],
                                                    request_body=CommodityGroupCategoryCreateSerializer,
                                                    responses={
                                                        200: CommodityGroupCategorySerializer(),
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

        serializer = CommodityGroupCategorySerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['commodity-groups-categories'],
                                                                responses={
                                                                    200: CommodityGroupCategorySimpleSerializer(
                                                                        many=True)
                                                                }))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        tags=['commodity-groups']
    )
)
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['commodity-groups']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['commodity-groups']))
class CommodityGroupViewSet(BaseViewSet,
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            GenericViewSet
                            ):
    queryset = CommodityGroup.objects.select_related(
        'shop'
    )
    serializer_class = CommodityGroupSerializer
    parser_classes = (DrfNestedParser,)
    serializers = {
        'create': CommodityGroupCreateSerializer,
        'update': CommodityGroupCreateSerializer,
        'products': ProductSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = CommodityGroupFilterSet
    permission_classes = [IsAdminOrReadOnly | IsManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'crm_user'):
            if user.crm_user.role == RoleType.ADMIN:
                pass
            elif user.crm_user.role == RoleType.MANAGER:
                queryset = queryset.filter(shop_id=user.crm_user.shop_id)

        return queryset

    def perform_create(self, serializer):
        commodity_product = add_commodity_group(serializer.validated_data)
        return commodity_product

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        commodity_product = update_commodity_group(pk, serializer.validated_data)
        return commodity_product

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_commodity_group(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(tags=['commodity-groups'],
                                                    request_body=CommodityGroupCreateSerializer,
                                                    responses={
                                                        200: CommodityGroupSerializer(),
                                                    }))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = CommodityGroupSerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(tags=['commodity-groups'],
                                                    request_body=CommodityGroupCreateSerializer,
                                                    responses={
                                                        200: CommodityGroupSerializer(),
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

        serializer = CommodityGroupSerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='products',
                      decorator=swagger_auto_schema(
                          tags=['commodity-groups'],
                          responses={
                              200: ProductSerializer(many=True),
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='products')
    def products(self, request, *args, **kwargs):
        instance = self.get_object()
        products = instance.products.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
