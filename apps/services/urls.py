from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.services.views import ServiceCategoryViewSet, ServiceViewSet

kid_services_router = DefaultRouter()
kid_services_router.register(prefix='categories', viewset=ServiceCategoryViewSet, basename='service-categories')
kid_services_router.register(prefix='', viewset=ServiceViewSet, basename='services')


urlpatterns = [
    path('', include(kid_services_router.urls))
]