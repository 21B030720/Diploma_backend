from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.orders.models import ClientOrder, OrderItem
from apps.shops.bundles.models import Bundle
from apps.shops.bundles.serializers import BundleDetailSerializer
from apps.shops.products.models import Product
from apps.shops.products.serializers import ProductSerializer
from apps.users.kids.models import Kid


class OrderItemSerializer(serializers.ModelSerializer): # for crm
    client_name = serializers.CharField(source='client_order.client_user.name')
    client_phone_number = serializers.CharField(source='client_order.client_user.phone_number')
    shop_name = serializers.CharField(source='shop.name')
    for_kid_name = serializers.CharField(source='for_kid.name', allow_null=True)

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'code',
            'client_name',
            'client_phone_number',
            'for_kid_id',
            'for_kid_name',
            'shop_id',
            'shop_name',
            'item_type',
            'discount',
            'final_price',
            'quantity',
            'created_at',
            'status'
        )


class OrderItemDetailSerializer(OrderItemSerializer):
    product = ProductSerializer()
    bundle = BundleDetailSerializer()

    class Meta:
        model = OrderItem
        fields = OrderItemSerializer.Meta.fields + (
            'product',
            'bundle'
        )


class ChangeOrderItemStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = (
            'status',
        )


class OrderItemForOrderSerializer(serializers.ModelSerializer): # for users
    product = serializers.SerializerMethodField()
    bundle = serializers.SerializerMethodField()
    shop_name = serializers.CharField(source='shop.name')
    for_kid_name = serializers.CharField(source='for_kid.name', allow_null=True)

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'code',
            'for_kid_id',
            'for_kid_name',
            'product',
            'bundle',
            'discount',
            'overall_price',
            'final_price',
            'quantity',
            'status',
            'shop_id',
            'shop_name',
            'item_type',
            'created_at'
        )

    @swagger_serializer_method(serializer_or_field=ProductSerializer())
    def get_product(self, obj):
        product = obj.product
        if product:
            return ProductSerializer(product).data
        return None

    @swagger_serializer_method(serializer_or_field=BundleDetailSerializer())
    def get_bundle(self, obj):
        bundle = obj.bundle
        if bundle:
            return BundleDetailSerializer(bundle).data
        return None


class OrderItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.values_list('id', flat=True), allow_null=True
    )
    bundle_id = serializers.PrimaryKeyRelatedField(
        queryset=Bundle.objects.values_list('id', flat=True), allow_null=True
    )
    for_kid_id = serializers.PrimaryKeyRelatedField(
        queryset=Kid.objects.values_list('id', flat=True), required=False, allow_null=True
    )

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product_id',
            'bundle_id',
            'for_kid_id',
            'discount',
            'quantity',
            'item_type'
        )


class ClientOrderSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(source='client_user.id')
    client_name = serializers.CharField(source='client_user.name')
    client_phone_number = serializers.CharField(source='client_user.phone_number')

    class Meta:
        model = ClientOrder
        fields = (
            'id',
            'idempotency',
            'client_id',
            'client_name',
            'client_phone_number',
            'discount',
            'overall_price',
            'final_price',
            'created_at',
            'status'
        )


class ClientOrderDetailSerializer(ClientOrderSerializer): #For users
    order_items = OrderItemForOrderSerializer(many=True, read_only=True)

    class Meta:
        model = ClientOrder
        fields = ClientOrderSerializer.Meta.fields + (
            'order_items',
        )


class ClientOrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = ClientOrder
        fields = (
            'order_items',
            'discount',
        )


class ChangeOrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientOrder
        fields = (
            'status',
        )