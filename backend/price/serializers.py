from rest_framework import serializers

from .models import Price
from catalog.models import Image
from catalog.serializers import PriceImageSerializer


class PriceSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="product.full_name", read_only=True)
    title_characteristic = serializers.CharField(source="characteristic.name", read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    count = serializers.IntegerField(default=0)

    def get_images(self, obj):
        images = Image.objects.filter(product=obj.product)
        if images:
            result = PriceImageSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Price
        fields = ["id", "product", "title", "characteristic", "title_characteristic", "price", "count", "images"]


class PriceDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="product.full_name", read_only=True)
    title_characteristic = serializers.CharField(source="characteristic.name", read_only=True)
    count = serializers.IntegerField(default=0, read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    description = serializers.CharField(source="product.description", read_only=True, default='')

    def get_images(self, obj):
        images = Image.objects.filter(product=obj.product)
        if images:
            result = PriceImageSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Price
        fields = [
            "id",
            "product",
            "characteristic",
            "title",
            "title_characteristic",
            "price",
            "count",
            "images",
            "description"
        ]

