from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.shops.bundles.filters import BundleFilterSet
from apps.shops.bundles.models import Bundle
from apps.shops.bundles.serializers import BundleSerializer, BundleCreateSerializer
from apps.shops.bundles.services import add_bundle, update_bundle, delete_bundle
from apps.shops.products.serializers import ProductSerializer
from apps.users.permissions import IsAdmin, IsManager, ReadOnly
from apps.utils.enums import RoleType
from apps.utils.filters import SortingFilterBackend
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        tags=['bundles']
    )
)
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
        'products': ProductSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = BundleFilterSet
    permission_classes = [IsAdmin | IsManager | ReadOnly]

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
                                                        200: BundleSerializer(),
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
                                                        200: BundleSerializer(),
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
                              200: ProductSerializer(many=True),
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='products')
    def products(self, request, *args, **kwargs):
        instance = self.get_object()
        products = instance.products.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
