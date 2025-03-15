from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.orders.views import ClientOrderViewSet, OrderItemViewSet

order_router = DefaultRouter()
order_router.register('order-items', viewset=OrderItemViewSet, basename='order-items')
order_router.register('', viewset=ClientOrderViewSet, basename='client-orders')

urlpatterns = [
    path('', include(order_router.urls))
]