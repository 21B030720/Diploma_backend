from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.wallets.views import WalletViewSet

wallet_router = DefaultRouter()
wallet_router.register(prefix='', viewset=WalletViewSet, basename='wallets')


urlpatterns = [
    path('', include(wallet_router.urls)),
]