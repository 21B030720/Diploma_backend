from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.kids.models import Kid
from apps.users.kids.serializers import KidSerializer, KidCreateSerializer
from apps.users.kids.services import add_kid, update_kid, delete_kid
from apps.users.permissions import IsClientUser
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        tags=['kids']
    )
)
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['kids']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['kids']))
class KidViewSet(BaseViewSet,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 GenericViewSet):
    queryset = Kid.objects.all()
    serializer_class = KidSerializer
    serializers = {
        'create': KidCreateSerializer,
        'update': KidCreateSerializer
    }
    parser_classes = (DrfNestedParser, JSONParser)

    permission_classes = [IsClientUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user
        if hasattr(user, 'client_user'):
            context['user'] = user
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'client_user'):
            queryset = queryset.filter(client_user=user.client_user)
        return queryset

    def perform_create(self, serializer):
        client_user = self.request.user.client_user
        shop = add_kid(client_user, serializer.validated_data)
        return shop

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        shop = update_kid(pk, serializer.validated_data)
        return shop

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_kid(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(tags=['kids'],
                                                    responses={
                                                        201: KidSerializer(),
                                                    }))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = KidSerializer(objs, context=self.get_serializer_context())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(tags=['kids'],
                                                    responses={
                                                        201: KidSerializer(),
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

        serializer = KidSerializer(instance=instance, context=self.get_serializer_context())
        return Response(serializer.data)
