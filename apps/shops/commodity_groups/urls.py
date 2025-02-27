from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.shops.commodity_groups.views import CommodityGroupCategoryViewSet, CommodityGroupViewSet

commodity_group_router = DefaultRouter()
commodity_group_router.register(prefix='categories', viewset=CommodityGroupCategoryViewSet, basename='commodity-groups-categories')
commodity_group_router.register(prefix='', viewset=CommodityGroupViewSet, basename='commodity_groups')


urlpatterns = [
    path('', include(commodity_group_router.urls)),
]