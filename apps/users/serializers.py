from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if hasattr(self.user, 'crm_user'):
            data['role'] = self.user.crm_user.role
        return data
