from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import CRMUser, User
from apps.users.permissions import IsAdminOrReadOnly
from apps.users.serializers import CustomTokenObtainPairSerializer, CRMUserSerializer, CRMUserCreateSerializer
from apps.users.services import create_user, update_user
from apps.utils.serializers import BadRequestSerializer
from apps.utils.views import BaseViewSet


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['users']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['users']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['users']))
class CRMUserViewSet(BaseViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = CRMUser.objects.all()
    serializer_class = CRMUserSerializer
    serializers = {
        'create': CRMUserCreateSerializer,
        'update': CRMUserCreateSerializer,
    }
    permission_classes = [IsAdminOrReadOnly]

    def check_permissions(self, request):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().check_permissions(request)

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def perform_create(self, serializer):
        user = create_user(serializer.validated_data)
        return user

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        updated_user = update_user(pk, serializer.validated_data)
        return updated_user

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        crm_user = CRMUser.objects.filter(pk=pk).first()
        crm_user.shops.clear()
        CRMUser.objects.filter(pk=pk).update(deleted=True, role=None)
        User.objects.filter(pk=crm_user.user.pk).update(deleted=True)

    @method_decorator(name='create',
                      decorator=swagger_auto_schema(tags=['users'],
                                                    request_body=CRMUserCreateSerializer(),
                                                    responses={
                                                        200: CRMUserSerializer(),
                                                        400: openapi.Response(
                                                            description="Bad Request",
                                                            schema=BadRequestSerializer()
                                                        )
                                                    }))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        serializer = CRMUserSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(name='update',
                      decorator=swagger_auto_schema(tags=['users'],
                                                    request_body=CRMUserCreateSerializer(),
                                                    responses={
                                                        200: CRMUserSerializer(),
                                                        400: openapi.Response(
                                                            description="Bad Request",
                                                            schema=BadRequestSerializer()
                                                        )
                                                    }))
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        serializer = CRMUserSerializer(instance=instance)

        return Response(serializer.data)
