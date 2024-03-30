from uuid import uuid4
from rest_framework import serializers
from .models import (
    TypesOfProducts,
    Products,
    ProductsGroup,
    Images,
    Characteristics,
    Organizations,
    Partners,
    Contractors,
    Agreements,
    Contracts
)

from debug import IsDebug, IsDeepDebug, IsPrintExceptions, print_exception, print_to

class TypesOfProductsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = TypesOfProducts
        fields = ['id', 'name']


class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Products
        fields = ["id", "full_name", "group", "use_characteristic", "type_of_product"]


class ProductDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)
    images = serializers.SerializerMethodField(read_only=True)
    count = serializers.IntegerField(default=0, read_only=True)

    def get_images(self, obj):
        images = Images.objects.filter(product=obj.id)
        if images:
            result = PriceImagesSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Products
        fields = ['id', 'full_name', 'description', 'images', 'count']


class CharacteristicsDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4, source='product.id')
    full_name = serializers.CharField(source='product.full_name')
    description = serializers.CharField(source='product.description')
    images = serializers.SerializerMethodField(read_only=True)
    title_characteristic = serializers.CharField(source='name')
    characteristic = serializers.UUIDField(default=uuid4, source='id')

    def get_images(self, obj):
        images = Images.objects.filter(product=obj.product)
        if images:
            result = PriceImagesSerializer(images, many=True)
            return result.data
        return []

    class Meta:
        model = Characteristics
        fields = ['id', 'full_name', 'description', 'images', 'title_characteristic', 'characteristic']


class ProductsGroupSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = ProductsGroup
        fields = ["id", "title", "parent"]


class ImagesSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Images
        fields = ["id", "product", "image"]

    def save(self, **kwargs):
        response = None
        try:
            request = self.context.get('request', None)
            #if self.instance and self.instance.image:
            #    self.instance.image.delete()
            if self.is_valid(raise_exception=True):
                response = super().save(**kwargs)
        except Exception as err:
            if IsPrintExceptions:
                print_exception(stack=True, request=request)
        return response


class CharacteristicsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Characteristics
        fields = ["id", "name", "product", "type_of_product"]


class OrganizationsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Organizations
        fields = ["id", "name"]


class PartnersSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Partners
        fields = ["id", "name", "full_name"]


class ContractorsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Contractors
        fields = ["id", "name", "full_name", "status", "inn", "kpp", "partner"]


class AgreementsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Agreements
        fields = ["id", "name", "number", "date", "partner", "contractor"]


class ContractsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)

    class Meta:
        model = Contracts
        fields = ["id", "name", "number", "date", "partner", "contractor", "organization", "default"]


class ProductsGroupTreeSerializer(serializers.Serializer):
    id = serializers.CharField()
    parent = serializers.CharField()
    title = serializers.CharField()
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        nodes = []
        for node in obj.children:
            result = ProductsGroupTreeSerializer(node)
            nodes.append(result.data)
        return nodes


class PriceImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["image"]
