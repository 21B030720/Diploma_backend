from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.shops.bundles.views import BundleViewSet

bundles_router = DefaultRouter()
bundles_router.register(prefix='', viewset=BundleViewSet, basename='bundles')


urlpatterns = [
    path('', include(bundles_router.urls)),
]