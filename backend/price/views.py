from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
import django_filters
from django.db.models import Q

from general_methods.mixins import general_response, StandardResultsSetPagination
from catalog.models import Product, Characteristic
from .serializers import PriceSerializer, PriceDetailSerializer
from .permissions import IsAdminOrReadOnly
from .models import Price

from debug import IsDebug, IsDeepDebug, IsPrintExceptions, print_exception, print_to

#   ----------
#   ПРАЙС-ЛИСТ
#   ----------


class PriceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="custom_filter")
    price = django_filters.RangeFilter()
    group = django_filters.CharFilter(field_name="product__group")

    class Meta:
        model = Price
        fields = ["search", "price", "group"]

    def custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(product__full_name__contains=value) |
            Q(characteristic__name__contains=value)
        )


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filterset_class = PriceFilter

    def create(self, request, *args, **kwargs):
        try:
            product = Product.objects.filter(pk=request.data["product"])
            if not product.exists():
                return Response(
                    {"results": None, "errors": "Номенклатуры нет на портале"},
                    status=status.HTTP_404_NOT_FOUND
                )
            characteristic = Characteristic.objects.filter(pk=request.data["characteristic"])
            price = request.data["price"]

            obj_product = product.get()
            obj_characteristic = characteristic.get() if len(characteristic) > 0 else None

            if price == 0:
                self.queryset.filter(product=obj_product, characteristic=obj_characteristic).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            product_price = self.queryset.filter(product=obj_product, characteristic=obj_characteristic)
            if product_price.exists():
                obj = product_price.get()
                obj.price = price
                obj.save()
                return Response(status=status.HTTP_206_PARTIAL_CONTENT)

            obj = self.queryset.create(product=obj_product, characteristic=obj_characteristic, price=price)
            obj.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as ex:
            if IsPrintExceptions:
                print_exception(stack=True, request=request)

            return Response(data={"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailViewSet(APIView):
    def get(self, request):
        request_id = request.query_params.get('id')
        queryset = Price.objects.filter(id=request_id).get()
        serializer = PriceDetailSerializer(queryset)
        return Response({'results': serializer.data, 'errors': ''}, status=status.HTTP_200_OK)

