from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.reviews.models import ObjectRating
from apps.reviews.serializers import ObjectRatingCRMSerializer
from apps.reviews.services import delete_rating
from apps.users.permissions import IsAdmin
from apps.utils.enums import ObjectRatingStatus
from apps.utils.filters import SortingFilterBackend
from apps.utils.serializers import EmptySerializer
from apps.utils.swagger_params import sort_param
from apps.utils.views import BaseViewSet


# Create your views here.
@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        tags=['reviews'],
        manual_parameters=[
            sort_param
        ]
    )
)
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['reviews']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['reviews']))
class ObjectRatingViewSet(BaseViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet
                          ):
    queryset = ObjectRating.objects.all()
    serializer_class = ObjectRatingCRMSerializer
    serializers = {
        'approve': EmptySerializer,
        'decline': EmptySerializer,
    }
    permission_classes = [IsAdmin]
    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    sorting_fields = {
    }

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_rating(pk)

    @method_decorator(name='approve',
                      decorator=swagger_auto_schema(
                          tags=['reviews'],
                          responses={
                              204: EmptySerializer(),
                          }
                      ))
    @action(detail=True, methods=['POST'], url_path='approve')
    def approve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = ObjectRatingStatus.APPROVED
        obj.save(update_fields=['status'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_decorator(name='decline',
                      decorator=swagger_auto_schema(
                          tags=['reviews'],
                          responses={
                              204: EmptySerializer(),
                          }
                      ))
    @action(detail=True, methods=['POST'], url_path='decline')
    def decline(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = ObjectRatingStatus.DECLINED
        obj.save(update_fields=['status'])
        return Response(status=status.HTTP_204_NO_CONTENT)
