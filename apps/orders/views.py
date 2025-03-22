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

from apps.orders.filters import ClientOrderFilterSet, OrderItemFilterSet
from apps.orders.models import ClientOrder, OrderItem
from apps.orders.serializers import ClientOrderSerializer, ClientOrderCreateSerializer, ClientOrderDetailSerializer, \
    OrderItemSerializer, OrderItemDetailSerializer, ChangeOrderItemStatusSerializer, ChangeOrderStatusSerializer
from apps.orders.services import create_order, change_order_item_status, change_order_status
from apps.users.permissions import IsClientUser, IsManager, IsAdmin
from apps.utils.enums import RoleType, OrderItemStatus, OrderStatus
from apps.utils.filters import SortingFilterBackend
from apps.utils.swagger_params import sort_param, shop_id_param
from apps.utils.views import BaseViewSet


# Create your views here.
@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      tags=['client-orders'],
                      manual_parameters=[
                          sort_param,
                      ]
                  ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['client-orders']))
class ClientOrderViewSet(BaseViewSet,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         GenericViewSet
                         ):
    queryset = ClientOrder.objects.select_related(
        'client_user',
    ).prefetch_related(
        'order_items__product',
        'order_items__bundle',
        'order_items__shop'
    ).order_by(
        '-created_at'
    )
    serializer_class = ClientOrderSerializer
    serializers = {
        'create': ClientOrderCreateSerializer,
        'retrieve': ClientOrderDetailSerializer,
        'change_status': ChangeOrderStatusSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = ClientOrderFilterSet
    sorting_fields = {

    }
    parser_classes = (JSONParser,)
    permission_classes = [IsClientUser | IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'crm_user'):
            if user.crm_user.role == RoleType.ADMIN:
                pass
        elif hasattr(user, 'client_user'):
            queryset = queryset.filter(client_user=user.client_user)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'cmr_user'):
            raise ValidationError("Only clients can create orders.")
        order = create_order(user, serializer.validated_data)
        return order

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(tags=['client-orders'],
                                                    request_body=ClientOrderCreateSerializer,
                                                    responses={
                                                        201: ClientOrderSerializer(),
                                                    }))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        serializer = ClientOrderSerializer(obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='change_status',
                      decorator=swagger_auto_schema(
                          tags=['client-orders'],
                          responses={
                              201: ClientOrderSerializer(),
                          }
                      ))
    @action(detail=True, methods=['PUT'], url_path='update-status')
    def change_status(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_ = serializer.validated_data.get('status')
        obj = self.get_object()
        order_item = change_order_status(obj, status_)
        serializer = ClientOrderSerializer(order_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      tags=['order-items'],
                      manual_parameters=[
                          shop_id_param,
                          sort_param
                      ]
                  ))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['order-items']))
class OrderItemViewSet(BaseViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = OrderItem.objects.select_related(
        'client_order',
        'shop',
        'product',
        'bundle'
    ).order_by('-created_at')
    serializer_class = OrderItemSerializer
    serializers = {
        'retrieve': OrderItemDetailSerializer,
        'change_status': ChangeOrderItemStatusSerializer
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = OrderItemFilterSet
    sorting_fields = {
        'client_name': 'client_order__client_user__name',
        'client_phone_number': 'client_order__client_user__phone_number',
        'shop_name': 'shop__name',
    }
    parser_classes = (JSONParser,)
    permission_classes = [IsAdmin | IsManager]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'crm_user'):
            if user.crm_user.role == RoleType.ADMIN:
                pass
            elif user.crm_user.role == RoleType.MANAGER:
                shop_id = user.crm_user.shop_id
                queryset = queryset.filter(shop_id=shop_id)
        else:
            queryset = queryset.filter(client_order__client_user_id=self.request.user.client_user.id)

        shop_ids = self.request.query_params.getlist('shop_id', [])
        if shop_ids:
            queryset = queryset.filter(shop_id__in=shop_ids)

        return queryset

    @method_decorator(name='change_status',
                      decorator=swagger_auto_schema(
                          tags=['order-items'],
                          responses={
                              201: OrderItemSerializer(),
                          }
                      ))
    @action(detail=True, methods=['PUT'], url_path='update-status', permission_classes=[IsAdmin | IsManager | IsClientUser])
    def change_status(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_ = serializer.validated_data.get('status')
        obj = self.get_object()
        order_item = change_order_item_status(obj, status_)
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
