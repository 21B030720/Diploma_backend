from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.shops.models import Shop
from apps.users.models import CRMUser, User


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
            'shop',
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
    password = serializers.CharField(max_length=25, required=False, allow_null=True, allow_blank=True)
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
