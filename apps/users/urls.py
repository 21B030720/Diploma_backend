from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import CustomTokenObtainPairView, CRMUserViewSet, CustomClientTokenObtainPairView, \
    ClientUserViewSet

user_router = DefaultRouter()
user_router.register(prefix='', viewset=CRMUserViewSet, basename='users')

client_router = DefaultRouter()
client_router.register(prefix='', viewset=ClientUserViewSet, basename='clients')

urlpatterns = [
    path('crm/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('crm/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('client/token/refresh/', CustomClientTokenObtainPairView.as_view(), name='client_token_refresh'),
    path('client/', include(client_router.urls)),
    path('', include(user_router.urls)),
]