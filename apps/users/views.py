from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.filters import CRMUserFilterSet, ClientUserFilterSet
from apps.users.models import CRMUser, User, ClientUser
from apps.users.permissions import IsAdmin, IsClientUser
from apps.users.serializers import CustomTokenObtainPairSerializer, CRMUserSerializer, CRMUserCreateSerializer, \
    CustomMobileTokenObtainPairSerializer, ClientUserSerializer, ClientUserCreateSerializer, ClientUserSignInSerializer, \
    ClientUserSignInResponseSerializer
from apps.users.services import create_user, update_user, create_client_user
from apps.utils.enums import RoleType
from apps.utils.filters import SortingFilterBackend
from apps.utils.serializers import BadRequestSerializer
from apps.utils.views import BaseViewSet


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class CustomClientTokenObtainPairView(APIView):
    serializer_class = CustomMobileTokenObtainPairSerializer

    @swagger_auto_schema(request_body=CustomMobileTokenObtainPairSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        refresh_token = data.get('refresh')
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                user_id = refresh.payload.get('user_id')
                user = User.objects.get(pk=user_id)
                new_refresh = RefreshToken.for_user(user)
                access_token = str(new_refresh.access_token)
                refresh_token_new = str(new_refresh)
            except Exception as e:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token_new,
            }, status=status.HTTP_200_OK)
        return ValidationError('Refresh token not provided')


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
    filter_backends = (DjangoFilterBackend, SortingFilterBackend)
    filterset_class = CRMUserFilterSet
    permission_classes = [IsAdmin]

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
        CRMUser.objects.filter(pk=pk).update(deleted=True)
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
        crm_user = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        serializer = CRMUserSerializer(instance=crm_user)

        return Response(serializer.data)


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['client-users']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['client-users']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['client-users']))
class ClientUserViewSet(BaseViewSet,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer

    serializers = {
        'sign_up': ClientUserCreateSerializer,
        'sign_in': ClientUserSignInSerializer
    }
    filter_backends = (DjangoFilterBackend, SortingFilterBackend)
    filterset_class = ClientUserFilterSet
    permission_classes = [IsAdmin | IsClientUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'client_user'):
            queryset = queryset.filter(user=user.id)
        return queryset

    @method_decorator(name='sign_up',
                      decorator=swagger_auto_schema(
                          tags=['client-users'],
                          responses={
                              201: ClientUserSerializer(),
                          },
                          permission_classes=[AllowAny]
                      ))
    @action(methods=['POST'], detail=False, url_path='sign-up', permission_classes=[AllowAny])
    def sign_up(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_user = create_client_user(serializer.validated_data)
        serializer = ClientUserSerializer(client_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(name='sign_in',
                      decorator=swagger_auto_schema(
                          tags=['client-users'],
                          responses={
                              200: ClientUserSignInResponseSerializer(),
                          },
                          permission_classes=[AllowAny]
                      ))
    @action(methods=['POST'], detail=False, url_path='sign-in', permission_classes=[AllowAny])
    def sign_in(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        client_user = ClientUser.objects.filter(
            (Q(email__iexact=username_or_email) & Q(is_email_valid=True)) | Q(user__username__iexact=username_or_email)
        ).first()

        if not client_user:
            raise ValidationError("Invalid credentials", code=401)

        authenticated_user = authenticate(username=client_user.user.username, password=password)
        if not authenticated_user:
            raise ValidationError("Invalid credentials", code=401)

        refresh = RefreshToken.for_user(authenticated_user)
        access_token = str(refresh.access_token)

        data = {
            'access_token': access_token,
            'refresh_token': str(refresh),
            'client_id': client_user.id,
            'user_id': client_user.user.id,
            'username': client_user.user.username,
        }

        serializer = ClientUserSignInResponseSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
