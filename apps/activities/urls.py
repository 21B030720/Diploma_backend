from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.activities.views import EventCategoryViewSet, EventViewSet, CourseCategoryViewSet, CourseViewSet

event_router = DefaultRouter()
event_router.register(prefix='categories', viewset=EventCategoryViewSet, basename='event-categories')
event_router.register(prefix='', viewset=EventViewSet, basename='events')

course_router = DefaultRouter()
course_router.register(prefix='categories', viewset=CourseCategoryViewSet, basename='course-categories')
course_router.register(prefix='', viewset=CourseViewSet, basename='courses')


urlpatterns = [
    path('events/', include(event_router.urls)),
    path('courses/', include(course_router.urls))
]