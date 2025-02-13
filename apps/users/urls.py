from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import CustomTokenObtainPairView, CRMUserViewSet

user_router = DefaultRouter()
user_router.register(prefix='', viewset=CRMUserViewSet, basename='users')

urlpatterns = [
    path('crm/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('crm/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(user_router.urls)),
]