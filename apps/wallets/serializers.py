from rest_framework import serializers

from apps.wallets.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    client_user_name = serializers.CharField(source='client_user.name')

    class Meta:
        model = Wallet
        fields = (
            'id',
            'client_user_name',
            'balance'
        )


class WalletTopUpSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            'id',
            'amount',
            'wallet',
            'transaction_type',
            'status',
            'created_at',
        )
