from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from general_methods.mixins import GeneralModelViewSet
from .serializers import (
    TypesOfProductsSerializer,
    ProductsSerializer,
    ProductsGroupSerializer,
    ProductsGroupTreeSerializer,
    ImagesSerializer,
    CharacteristicsSerializer,
    OrganizationsSerializer,
    PartnersSerializer,
    ContractorsSerializer,
    AgreementsSerializer,
    ContractsSerializer,
)
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

#   -------------------------
#   НОМЕНКЛАТУРА. СПРАВОЧНИКИ
#   -------------------------


class TypesOfProductsViewSet(GeneralModelViewSet):
    queryset = TypesOfProducts.objects.all()
    serializer_class = TypesOfProductsSerializer


class ProductsViewSet(GeneralModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class ProductsGroupViewSet(GeneralModelViewSet):
    queryset = ProductsGroup.objects.all()
    serializer_class = ProductsGroupSerializer


class ImagesViewSet(GeneralModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class CharacteristicsViewSet(GeneralModelViewSet):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicsSerializer


class OrganizationsViewSet(GeneralModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationsSerializer


class PartnersViewSet(GeneralModelViewSet):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializer


class ContractorsViewSet(GeneralModelViewSet):
    serializer_class = ContractorsSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Contractors.objects.all()
        elif self.request.user:
            return Contractors.objects.filter(id=self.request.user.contractor)


class AgreementsViewSet(GeneralModelViewSet):
    serializer_class = AgreementsSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Agreements.objects.all()
        elif self.request.user:
            return Agreements.objects.filter(contractor=self.request.user.contractor)


class ContractsViewSet(GeneralModelViewSet):
    serializer_class = ContractsSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Contracts.objects.all()
        elif self.request.user:
            return Contracts.objects.filter(contractor=self.request.user.contractor)


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


class ProductsGroupTree(APIView):
    def get(self, request):
        tree_nodes = collect_nodes(ProductsGroup.objects.all())
        root_nodes = list(filter(lambda nd: nd.parent is None, tree_nodes.values()))

        result = []
        for node in root_nodes:
            group_sr = ProductsGroupTreeSerializer(node)
            result.append(group_sr.data)

        return Response({"results": result, "errors": None}, status=status.HTTP_200_OK)
