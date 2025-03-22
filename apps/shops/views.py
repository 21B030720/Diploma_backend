from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.reviews.serializers import RateSerializer, ObjectRatingSerializer
from apps.shops.filters import ShopFilterSet, CityFilterSet, CountryFilterSet
from apps.shops.models import Shop, City, Country
from apps.shops.serializers import ShopSerializer, ShopCreateSerializer, ShopSimpleSerializer, CitySerializer, \
    CityCreateSerializer, CitySimpleSerializer, CountrySerializer, CountryCreateSerializer
from apps.shops.services import add_shop, add_city, update_city, delete_city, add_country, update_country, \
    delete_country, delete_shop, update_shop, rate_shop
from apps.users.models import CRMUser
from apps.users.permissions import IsAdmin, IsManager, ReadOnly, IsClientUser
from apps.utils.enums import RoleType
from apps.utils.filters import SortingFilterBackend
from apps.utils.serializers import EmptySerializer
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['countries']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['countries']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['countries']))
class CountryViewSet(BaseViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet
                     ):
    serializer_class = CountrySerializer
    serializers = {
        'create': CountryCreateSerializer,
        'update': CountryCreateSerializer,
        'destroy': EmptySerializer,
        'all': CountrySerializer,
    }
    permission_classes = [IsAdmin | ReadOnly]
    queryset = Country.objects.order_by('name')
    filter_backends = (filters.DjangoFilterBackend, SortingFilterBackend)
    filterset_class = CountryFilterSet

    def perform_create(self, serializer):
        country = add_country(serializer.validated_data)
        return country

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        city = update_country(pk, serializer.validated_data)
        return city

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_country(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(
                          tags=['countries'],
                          responses={
                              200: CountrySerializer()
                          }
                      ))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = CountrySerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(
                          tags=['countries'],
                          responses={
                              200: CountrySerializer()
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

        serializer = CountrySerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['countries']))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['cities']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['cities']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['cities']))
class CityViewSet(
    BaseViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = CitySerializer
    serializers = {
        'create': CityCreateSerializer,
        'update': CityCreateSerializer,
        'destroy': EmptySerializer,
        'all': CitySimpleSerializer,
    }
    permission_classes = [IsAdmin | ReadOnly]
    queryset = City.objects.all().order_by('name')
    filter_backends = (filters.DjangoFilterBackend, SortingFilterBackend)
    filterset_class = CityFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def perform_create(self, serializer):
        city = add_city(serializer.validated_data)
        return city

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        city = update_city(pk, serializer.validated_data)
        return city

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        delete_city(pk)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(
                          tags=['cities'],
                          responses={
                              200: CitySerializer()
                          })
                      )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objs = self.perform_create(serializer)
        serializer = CitySerializer(objs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(
                          tags=['cities'],
                          responses={
                              200: CitySerializer()
                          })
                      )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer = CitySerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['cities']))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        tags=['shops']
    )
)
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['shops']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['shops']))
class ShopViewSet(BaseViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet
                  ):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    parser_classes = (DrfNestedParser, )

    serializers = {
        'create': ShopCreateSerializer,
        'update': ShopCreateSerializer,
        'all': ShopSimpleSerializer,
        'rate_shop': RateSerializer
    }
    permission_classes = [IsAdmin | IsManager | ReadOnly]

    filter_backends = (SortingFilterBackend, filters.DjangoFilterBackend)
    filterset_class = ShopFilterSet

    sorting_fields = {
        'city_name': 'city__name'
    }

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user
        if user.is_authenticated:
            context['user'] = user
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if hasattr(user, 'crm_user'):
            crm_user = user.crm_user
            if crm_user.role == RoleType.ADMIN:
                pass
            else:
                queryset = queryset.filter(id=crm_user.shop.id)

        return queryset

    def perform_create(self, serializer):
        shop = add_shop(serializer.validated_data)
        return shop

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        shop = update_shop(pk, serializer.validated_data)
        return shop

    def perform_destroy(self, instance):
        user = self.request.user
        crm_user = user.crm_user
        if crm_user.role == RoleType.ADMIN:
            pk = self.kwargs['pk']
            delete_shop(pk)
        else:
            raise ValidationError('Only admin can delete shops.')

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(tags=['shops'],
                                                    request_body=ShopCreateSerializer,
                                                    responses={
                                                        200: ShopSerializer(),
                                                    }))
    def create(self, request, *args, **kwargs):
        user = self.request.user
        crm_user = user.crm_user
        if crm_user.role == RoleType.ADMIN:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            objs = self.perform_create(serializer)
            serializer = ShopSerializer(objs)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            raise ValidationError('Only admin can add shops')

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(tags=['shops'],
                                                    request_body=ShopCreateSerializer,
                                                    responses={
                                                        200: ShopSerializer(),
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

        serializer = ShopSerializer(instance=instance)
        return Response(serializer.data)

    @method_decorator(name='all', decorator=swagger_auto_schema(tags=['shops'],
                                                                responses={
                                                                    200: ShopSimpleSerializer(many=True)
                                                                }))
    @action(methods=['GET'], detail=False, url_path='all')
    def all(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @method_decorator(name='rate_shop',
                      decorator=swagger_auto_schema(
                          tags=['shops'],
                          responses={
                              201: ShopSerializer()
                          }
                      ))
    @action(methods=['POST'], detail=True, url_path='rate-shop', permission_classes=[IsClientUser], parser_classes=(JSONParser, ))
    def rate_shop(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.get_object()
        user = self.request.user
        service_provider = rate_shop(obj, user, serializer.validated_data)
        serializer = ShopSerializer(service_provider, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(name='shop_reviews',
                      decorator=swagger_auto_schema(
                          tags=['shops'],
                          responses={
                              200: ObjectRatingSerializer(many=True)
                          }
                      ))
    @action(methods=['GET'], detail=True, url_path='shop-reviews')
    def shop_reviews(self, request, *args, **kwargs):
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
                          tags=['shops'],
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
