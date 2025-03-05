from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.shops.models import Shop
from apps.users.models import CRMUser, User, ClientUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if hasattr(self.user, 'crm_user'):
            data['role'] = self.user.crm_user.role
        return data


class CustomMobileTokenObtainPairSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


class CRMUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()

    class Meta:
        model = CRMUser
        fields = (
            'id',
            'username',
            'name',
            'phone_number',
            'role',
            'shop_id',
            'shop_name'
        )

    def get_username(self, obj):
        return obj.user.username

    def get_shop_name(self, obj):
        try:
            return obj.user.shop.name
        except AttributeError:
            return None


class CRMUserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=25)
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.values_list('id', flat=True))

    class Meta:
        model = CRMUser
        fields = (
            'username',
            'password',
            'shop_id',
            'name',
            'phone_number',
            'role',
        )

    def to_internal_value(self, data):
        """Move fields related to operation to their own operation dictionary."""
        user_internal = {}

        internal = super().to_internal_value(data)

        for key in UserSerializer.Meta.fields:
            if key in internal:
                user_internal[key] = internal.pop(key)

        internal['user'] = user_internal

        return internal


class ClientUserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=25)

    class Meta:
        model = ClientUser
        fields = (
            'username',
            'password',
            'phone_number',
            'name',
            'email',
        )

    def to_internal_value(self, data):
        """Move fields related to operation to their own operation dictionary."""
        user_internal = {}

        internal = super().to_internal_value(data)

        for key in UserSerializer.Meta.fields:
            if key in internal:
                user_internal[key] = internal.pop(key)

        internal['user'] = user_internal

        return internal


class ClientUserSignInSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=25)


class ClientUserSignInResponseSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
    client_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()


class ClientUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = ClientUser
        fields = (
            'id',
            'username',
            'name',
            'phone_number',
            'email',
            'is_email_valid'
        )
