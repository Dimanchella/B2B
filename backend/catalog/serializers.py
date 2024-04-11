from uuid import uuid4
from rest_framework import serializers
from .models import (
    TypeOfProduct,
    Product,
    ProductGroup,
    Image,
    Characteristic,
    Organization,
    Partner,
    Contractor,
    Agreement,
    Contract
)

from debug import IsDebug, IsDeepDebug, IsPrintExceptions, print_exception, print_to

class TypeOfProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = TypeOfProduct
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Product
        fields = ["id", "full_name", "group", "use_characteristic", "type_of_product"]


class ProductDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)
    images = serializers.SerializerMethodField(read_only=True)
    count = serializers.IntegerField(default=0, read_only=True)

    def get_images(self, obj):
        images = Image.objects.filter(product=obj.id)
        if images:
            result = PriceImageSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Product
        fields = ['id', 'full_name', 'description', 'images', 'count']


class CharacteristicDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4, source='product.id')
    full_name = serializers.CharField(source='product.full_name')
    description = serializers.CharField(source='product.description')
    images = serializers.SerializerMethodField(read_only=True)
    title_characteristic = serializers.CharField(source='name')
    characteristic = serializers.UUIDField(default=uuid4, source='id')

    def get_images(self, obj):
        images = Image.objects.filter(product=obj.product)
        if images:
            result = PriceImageSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Characteristic
        fields = ['id', 'full_name', 'description', 'images', 'title_characteristic', 'characteristic']


class ProductGroupSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = ProductGroup
        fields = ["id", "title", "parent"]


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Image
        fields = ["id", "product", "image"]

    def save(self, **kwargs):
        response = None
        request = self.context.get('request', None)
        try:
            #if self.instance and self.instance.image:
            #    self.instance.image.delete()
            if self.is_valid(raise_exception=True):
                response = super().save(**kwargs)
        except Exception as err:
            if IsPrintExceptions:
                print_exception(stack=True, request=request)
        return response


class CharacteristicSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Characteristic
        fields = ["id", "name", "product", "type_of_products"]


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Organization
        fields = ["id", "name"]


class PartnerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Partner
        fields = ["id", "name", "full_name"]


class ContractorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Contractor
        fields = ["id", "name", "full_name", "status", "inn", "kpp", "partner"]


class AgreementSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Agreement
        fields = ["id", "name", "number", "date", "partner", "contractor"]


class ContractSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Contract
        fields = ["id", "name", "number", "date", "partner", "contractor", "organization", "default"]


class ProductGroupTreeSerializer(serializers.Serializer):
    id = serializers.CharField()
    parent = serializers.CharField()
    title = serializers.CharField()
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        nodes = []
        for node in obj.children:
            result = ProductGroupTreeSerializer(node)
            nodes.append(result.data)
        return nodes


class PriceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]

