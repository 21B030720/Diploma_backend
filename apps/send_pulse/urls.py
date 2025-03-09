from django.urls import path

from apps.send_pulse.views import ConfirmEmailAPIView

urlpatterns = [
    path('confirm-email/', ConfirmEmailAPIView.as_view(), name='confirm-email'),
]