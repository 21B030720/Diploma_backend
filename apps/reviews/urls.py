from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.reviews.views import ObjectRatingViewSet

object_rating_router = DefaultRouter()
object_rating_router.register(prefix='', viewset=ObjectRatingViewSet, basename='reviews')


urlpatterns = [
    path('', include(object_rating_router.urls))
]