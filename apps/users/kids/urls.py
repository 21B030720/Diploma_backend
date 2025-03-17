from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.kids.views import KidViewSet

kid_router = DefaultRouter()
kid_router.register(prefix='', viewset=KidViewSet, basename='kids')

urlpatterns = [
    path('', include(kid_router.urls))
]