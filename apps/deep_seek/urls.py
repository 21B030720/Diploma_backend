from django.urls import path

from apps.deep_seek.views import OpenAiAPIView

urlpatterns = [
    path('send-message/', OpenAiAPIView.as_view(), name='openai-send-message'),
]
