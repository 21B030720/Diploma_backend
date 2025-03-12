from django.urls import path

from apps.deep_seek.views import DeepSeekAPIView

urlpatterns = [
    path('send-message/', DeepSeekAPIView.as_view(), name='deep_seek-send-message'),
]
