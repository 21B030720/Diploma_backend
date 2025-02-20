from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.shops.views import ShopViewSet, CityViewSet, CountryViewSet
from apps.users.views import CustomTokenObtainPairView, CRMUserViewSet

shop_router = DefaultRouter()
shop_router.register(prefix='country', viewset=CountryViewSet, basename='country')
shop_router.register(prefix='city', viewset=CityViewSet, basename='cities')
shop_router.register(prefix='', viewset=ShopViewSet, basename='shops')

urlpatterns = [
    path('products/', include('apps.shops.products.urls')),
    path('', include(shop_router.urls)),
]