from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from general_methods.mixins import GeneralModelViewSet
from .serializers import (
    TypeOfProductSerializer,
    ProductSerializer,
    ProductGroupSerializer,
    ProductGroupTreeSerializer,
    ImageSerializer,
    CharacteristicSerializer,
    OrganizationSerializer,
    PartnerSerializer,
    ContractorSerializer,
    AgreementSerializer,
    ContractSerializer,
)
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

#   -------------------------
#   НОМЕНКЛАТУРА. СПРАВОЧНИКИ
#   -------------------------


class TypeOfProductViewSet(GeneralModelViewSet):
    queryset = TypeOfProduct.objects.all()
    serializer_class = TypeOfProductSerializer


class ProductViewSet(GeneralModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductGroupViewSet(GeneralModelViewSet):
    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer


class ImageViewSet(GeneralModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CharacteristicViewSet(GeneralModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer


class OrganizationViewSet(GeneralModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class PartnerViewSet(GeneralModelViewSet):
    serializer_class = PartnerSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Partner.objects.all()
        elif self.request.user.contractor:
            return Partner.objects.filter(id=self.request.user.contractor.partner.id)


class ContractorViewSet(GeneralModelViewSet):
    serializer_class = ContractorSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Contractor.objects.all()
        elif self.request.user:
            return Contractor.objects.filter(id=self.request.user.contractor.id)


class AgreementViewSet(GeneralModelViewSet):
    serializer_class = AgreementSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Agreement.objects.all()
        elif self.request.user:
            return Agreement.objects.filter(contractor=self.request.user.contractor)


class ContractViewSet(GeneralModelViewSet):
    serializer_class = ContractSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Contract.objects.all()
        elif self.request.user:
            return Contract.objects.filter(contractor=self.request.user.contractor)


class Node(object):
    def __init__(self, node):
        self.id = node.id
        self.parent = node.parent
        self.title = node.title
        self.children = []


def add_node(tree_nodes, data):
    if data.id in tree_nodes.keys():
        return
    node = Node(data)
    tree_nodes[node.id] = node
    if node.parent is not None:
        add_node(tree_nodes, node.parent)
        if node not in tree_nodes[node.parent.id].children:
            tree_nodes[node.parent.id].children.append(node)


def collect_nodes(product_groups):
    tree_nodes = {}
    for group in product_groups:
        add_node(tree_nodes, group)
    return tree_nodes


class ProductGroupTree(APIView):
    def get(self, request):
        tree_nodes = collect_nodes(ProductGroup.objects.all())
        root_nodes = list(filter(lambda nd: nd.parent is None, tree_nodes.values()))

        result = []
        for node in root_nodes:
            group_sr = ProductGroupTreeSerializer(node)
            result.append(group_sr.data)

        return Response({"results": result, "errors": None}, status=status.HTTP_200_OK)

