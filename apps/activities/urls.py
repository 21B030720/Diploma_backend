from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.activities.views import EventCategoryViewSet, EventViewSet

event_router = DefaultRouter()
event_router.register(prefix='categories', viewset=EventCategoryViewSet, basename='event-categories')
event_router.register(prefix='', viewset=EventViewSet, basename='event')


urlpatterns = [
    path('events/', include(event_router.urls)),
]