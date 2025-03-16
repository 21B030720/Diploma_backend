import random
import string

from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.orders.models import OrderItem, ClientOrder
from apps.shops.bundles.models import Bundle
from apps.shops.products.models import Product
from apps.utils.enums import ItemType, OrderItemStatus, OrderStatus
from apps.wallets.services import wallet_withdrawal


@transaction.atomic
def create_order(user, data):
    client_user = user.client_user
    order_items = data.pop('order_items', [])
    overall_price = 0
    final_price = 0
    discount = data.get('discount', 0)
    client_order = ClientOrder.objects.create(
        client_user=client_user,
        overall_price=overall_price,
        final_price=final_price,
        **data
    )
    order_items_bulk = []
    for order_item in order_items:
        shop = None
        code = generate_unique_code_for_order_item(k=6)
        order_item_overall_price = 0
        order_item_final_price = 0
        order_item_discount = order_item.get('discount', 0)
        item_type = order_item.get('item_type')
        if item_type == ItemType.PRODUCT:
            product_id = order_item.get('product_id')
            product = Product.objects.get(id=product_id)
            product_price = product.price
            order_item_overall_price += product_price
            order_item_final_price += order_item_overall_price * (100 - order_item_discount) / 100
            shop = product.shop
        elif item_type == ItemType.BUNDLE:
            bundle_id = order_item.get('bundle_id')
            bundle = Bundle.objects.get(id=bundle_id)
            bundle_price = bundle.price
            order_item_overall_price += bundle_price
            order_item_final_price += order_item_overall_price * (100 - order_item_discount) / 100
            shop = bundle.shop

        overall_price += order_item_overall_price

        order_item_obj = OrderItem(
            code=code,
            client_order=client_order,
            shop=shop,
            overall_price=order_item_overall_price,
            final_price=order_item_final_price,
            **order_item
        )
        order_items_bulk.append(order_item_obj)

    final_price = overall_price * (100 - discount) / 100
    wallet_withdrawal(client_user.wallet, final_price)
    client_order.overall_price = overall_price
    client_order.final_price = final_price
    client_order.save(update_fields=['overall_price', 'final_price'])
    OrderItem.objects.bulk_create(order_items_bulk)
    return client_order


@transaction.atomic
def change_order_item_status(order_item, status):

    if order_item.status == OrderItemStatus.CANCELLED:
        return order_item

    order = order_item.client_order

    if status == OrderItemStatus.CANCELLED:
        client_user = order.client_user
        wallet_withdrawal(client_user.wallet, -order_item.final_price)
        order.final_price -= order_item.final_price
        order.save(update_fields=['final_price'])
        order_item.status = status
        order_item.save(update_fields=['status'])
    else:
        order_item.status = status
        order_item.save(update_fields=['status'])

        update_order_status(order)

    return order_item


@transaction.atomic
def change_order_status(order: ClientOrder, status):

    if order.status == OrderStatus.CANCELLED:
        raise ValidationError("This order is cancelled.")

    if status == OrderStatus.CANCELLED:
        order_items = order.order_items.exclude(status=OrderItemStatus.GIVEN_TO_CUSTOMER)
        for order_item in order_items:
            change_order_item_status(order_item, OrderItemStatus.CANCELLED)
    order.status = status

    order.save(update_fields=['status'])
    update_order_status(order)
    return order


def generate_unique_code_for_order_item(k=6):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
        if not OrderItem.objects.filter(code=code).exists():
            return code


def update_order_status(order):
    order_items = order.order_items.all()
    statuses = {item.status for item in order_items}

    if statuses == {OrderItemStatus.GIVEN_TO_CUSTOMER}:
        order.status = OrderStatus.TOTALLY_GIVEN
    elif statuses == {OrderItemStatus.GIVEN_TO_CUSTOMER, OrderItemStatus.CANCELLED}:
        order.status = OrderStatus.PARTIALLY_GIVEN
    else:
        order.status = OrderStatus.WAITING

    order.save(update_fields=['status'])
