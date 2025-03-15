from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.orders.models import ClientOrder
from apps.orders.serializers import ClientOrderSerializer, ClientOrderCreateSerializer, ClientOrderDetailSerializer
from apps.orders.services import create_order, delete_order
from apps.users.permissions import IsClientUser, IsManager, IsAdmin
from apps.utils.enums import RoleType
from apps.utils.filters import SortingFilterBackend
from apps.utils.swagger_params import sort_param
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
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['client-orders']))
class ClientOrderViewSet(BaseViewSet,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet
                         ):
    queryset = ClientOrder.objects.select_related(
        'client_user',
    ).prefetch_related(
        'order_items__product',
        'order_items__bundle',
        'order_items__shop'
    )
    serializer_class = ClientOrderSerializer
    parser_classes = (JSONParser, )
    serializers = {
        'create': ClientOrderCreateSerializer,
        'retrieve': ClientOrderDetailSerializer,
    }
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
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

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_order(pk)

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
