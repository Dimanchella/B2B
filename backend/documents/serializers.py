from uuid import uuid4
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from catalogs.models import Image
from catalogs.serializers import PriceImageSerializer
from .models import Order, OrdersDetail, ExchangeNode


class OrdersDetailSerializer(serializers.ModelSerializer):
    product_full_name = serializers.CharField(source="product.full_name", read_only=True)
    characteristic_name = serializers.CharField(source="characteristic.name", read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_images(self, obj):
        images = Image.objects.filter(product=obj.product)
        if images:
            result = PriceImageSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = OrdersDetail
        fields = [
            "pk",
            "order",
            "product",
            "product_full_name",
            "characteristic",
            "characteristic_name",
            "images",
            "price",
            "quantity",
            "total"
        ]


class OrderSerializer(WritableNestedModelSerializer):
    id = serializers.UUIDField(default=uuid4)
    order_orders_detail = OrdersDetailSerializer(many=True, required=False)
    partner_full_name = serializers.CharField(source="partner.full_name", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    contractor_name = serializers.CharField(source="contractor.name", read_only=True)

    def create(self, validated_data):
        order = super().create(validated_data)
        if self.initial_data.get("from_frontend"):
            order.fix_exchange()
        return order

    def update(self, instance, validated_data):
        order = super().update(instance, validated_data)
        if self.initial_data.get("from_frontend"):
            order.fix_exchange()
        return order

    class Meta:
        model = Order
        fields = [
            "id",
            "date_time",
            "number",
            "site_status",
            "partner",
            "partner_full_name",
            "contractor",
            "contractor_name",
            "organization",
            "organization_name",
            "agreement",
            "contract",
            "order_orders_detail"
        ]


class ExchangeNodeSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = ExchangeNode
        fields = ["pk", "updated_at", "order"]
