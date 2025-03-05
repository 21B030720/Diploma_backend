from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.permissions import IsClientUser
from apps.utils.views import BaseViewSet
from apps.wallets.models import Wallet, Transaction
from apps.wallets.serializers import WalletSerializer, WalletTopUpSerializer, TransactionSerializer
from apps.wallets.services import create_transaction_for_deposit


# Create your views here.
class WalletViewSet(
    BaseViewSet,
    GenericViewSet,
):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    serializers = {
        'top_up': WalletTopUpSerializer,
        'transactions_history': TransactionSerializer,
    }

    permission_classes = [IsClientUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(client_user=user.client_user)
        return queryset

    @method_decorator(name='my',
                      decorator=swagger_auto_schema(
                          tags=['wallets']
                      ))
    @action(methods=['GET'], detail=False, url_path='my')
    def my(self, request):
        user = self.request.user
        wallet = get_object_or_404(Wallet, client_user=user.client_user)
        serializer = self.get_serializer(wallet)
        return Response(serializer.data)

    @method_decorator(name='top_up',
                      decorator=swagger_auto_schema(
                          tags=['wallets'],
                          responses={
                              201: TransactionSerializer()
                          }
                      ))
    @action(methods=['POST'], detail=False, url_path='top-up')
    def top_up(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet = get_object_or_404(Wallet, client_user=user.client_user)
        transaction = create_transaction_for_deposit(wallet, serializer.validated_data)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(name='transactions_history',
                      decorator=swagger_auto_schema(
                          tags=['wallets']
                      ))
    @action(methods=['GET'], detail=False, url_path='transactions-history')
    def transactions_history(self, request):
        user = self.request.user
        wallet = get_object_or_404(Wallet, client_user=user.client_user)
        transactions = Transaction.objects.filter(wallet=wallet)

        page = self.paginate_queryset(transactions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(transactions, many=True)

        return Response(serializer.data)
