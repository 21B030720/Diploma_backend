from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.shops.products.views import ProductCategoryViewSet

products_router = DefaultRouter()
products_router.register(prefix='categories', viewset=ProductCategoryViewSet, basename='products-categories')
# products_router.register(prefix='', viewset=ProductViewSet, basename='products')


urlpatterns = [
    path('', include(products_router.urls)),
]