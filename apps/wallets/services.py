from rest_framework.exceptions import ValidationError

from apps.utils.enums import TransactionType, TransactionStatus
from apps.wallets.models import Transaction, Wallet


def create_transaction_for_deposit(wallet, data):
    amount = data.pop('amount')
    if amount < 2000:
        raise ValidationError('Amount must be greater than or equal to 2000.')

    transaction = Transaction.objects.create(
        wallet=wallet,
        amount=amount,
        transaction_type=TransactionType.DEPOSIT,
        status=TransactionStatus.PENDING,
    )

    return transaction


def finish_transaction(instance: Transaction) -> Transaction:
    if instance.transaction_type == TransactionType.DEPOSIT:
        wallet = Wallet.objects.get(id=instance.wallet.id)
        wallet.balance += instance.amount
        print(wallet.balance)
        wallet.save(update_fields=['balance'])

    return instance
