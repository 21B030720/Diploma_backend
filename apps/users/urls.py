from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import CustomTokenObtainPairView

urlpatterns = [
    path('crm/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('crm/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]