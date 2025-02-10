from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import CustomTokenObtainPairSerializer


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()