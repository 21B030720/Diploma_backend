import uuid

from django.db import models
from django.db.models import Q, Sum

from apps.shops.bundles.models import Bundle
from apps.shops.models import Shop
from apps.shops.products.models import Product
from apps.users.models import ClientUser
from apps.utils.enums import ItemType, OrderStatus, OrderItemStatus
from apps.utils.models import DeletedMixin, TimestampMixin


# Create your models here.
class ClientOrder(DeletedMixin, TimestampMixin):
    idempotency = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    client_user = models.ForeignKey(ClientUser, on_delete=models.CASCADE, related_name='orders')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overall_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.WAITING)

    # @property
    # def current_final_price(self):
    #     order_items_final_price = self.order_items.filter(
    #         deleted=False
    #     ).exclude(
    #         status=OrderItemStatus.CANCELLED
    #     ).aggregate(final_price=Sum('final_price'))['final_price']
    #     print(order_items_final_price)
    #     return order_items_final_price


class OrderItem(DeletedMixin, TimestampMixin):
    code = models.CharField(max_length=6, db_index=True, unique=True)
    client_order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name='order_items')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', null=True)
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, related_name='order_items', null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overall_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=OrderItemStatus.choices, default=OrderItemStatus.WAITING_FOR_COURIER)
    item_type = models.CharField(choices=ItemType.choices)
