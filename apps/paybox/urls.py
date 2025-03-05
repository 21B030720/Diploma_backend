from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.paybox import views
from apps.paybox.views import CardViewSet

card_router = DefaultRouter()
card_router.register(prefix='', viewset=CardViewSet, basename='cards')

urlpatterns = [
    path('payment/init-payment/', views.InitPaymentAPI.as_view()),
    path('cards/', include(card_router.urls)),

    path('result/payment/', views.PaymentResultAPI.as_view()),
    path('result/card-save/', views.CardSaveResultAPI.as_view()),
    path('result/success/', views.PaymentResultSuccessAPI.as_view()),
    path('result/failure/', views.PaymentResultFailureAPI.as_view()),
]
