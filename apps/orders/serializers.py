from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.orders.models import ClientOrder, OrderItem
from apps.shops.bundles.models import Bundle
from apps.shops.bundles.serializers import BundleSerializer, BundleDetailSerializer
from apps.shops.products.models import Product
from apps.shops.products.serializers import ProductSerializer
from apps.users.serializers import ClientUserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    bundle = serializers.SerializerMethodField()
    shop_name = serializers.CharField(source='shop.name')

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'code',
            'product',
            'bundle',
            'discount',
            'overall_price',
            'final_price',
            'status',
            'shop_id',
            'shop_name',
            'item_type'
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

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product_id',
            'bundle_id',
            'discount',
            'item_type'
        )


class ClientOrderSerializer(serializers.ModelSerializer):
    client_user = ClientUserSerializer(read_only=True)

    class Meta:
        model = ClientOrder
        fields = (
            'id',
            'idempotency',
            'client_user',
            'discount',
            'overall_price',
            'final_price',
            'status'
        )


class ClientOrderDetailSerializer(serializers.ModelSerializer):
    client_user = ClientUserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = ClientOrder
        fields = (
            'id',
            'idempotency',
            'client_user',
            'discount',
            'overall_price',
            'final_price',
            'status',
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
