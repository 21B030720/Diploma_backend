from django.db import models

from apps.users.models import User, ClientUser
from apps.utils.enums import TransactionType, TransactionStatus
from apps.utils.models import DeletedMixin, TimestampMixin


# Create your models here.
class Wallet(DeletedMixin, TimestampMixin):
    client_user = models.OneToOneField(ClientUser, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Transaction(DeletedMixin, TimestampMixin):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(choices=TransactionType.choices, max_length=50)
    status = models.CharField(
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING
    )
