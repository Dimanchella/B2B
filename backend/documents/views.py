from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.http import HttpResponse

from general_methods.mixins import GeneralModelViewSet, general_response, StandardResultsSetPagination
from price.serializers import PriceSerializer
from .serializers import OrderSerializer, ExchangeNodeSerializer
from .models import Order, ExchangeNode, OrdersDetail
from .tasks import upload_orders

from debug import IsDebug, IsDeepDebug, IsPrintExceptions, print_exception, print_to


#   ------
#   ЗАКАЗЫ
#   ------

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Order.objects.all().order_by('-date_time')
        elif self.request.user:
            return Order.objects.filter(contractor=self.request.user.contractor).order_by('-date_time')

    def update(self, request, *args, **kwargs):
        if IsDebug:
            print_to(None, 'OrdersViewSet.update: %s' % request.data)
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # new_order = Orders.objects.filter(contractor=self.request.user.contractor, site_status=SiteOrderStatus.CREATED)
        # if new_order:
        #     return general_response(
        #         errors="В базе есть созданный и не обработанный заказ",
        #         response_status=status.HTTP_400_BAD_REQUEST
        #     )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return general_response(
            serializer.data,
            response_status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        partner = self.request.data.get('partner')
        contractor = self.request.data.get('contractor')
        if contractor is None:
            serializer.save(contractor=self.request.user.contractor)
        elif partner is None and contractor.partner is not None:
            serializer.save(partner=self.request.user.contractor.partner)


class ExchangeNodeViewSet(GeneralModelViewSet):
    queryset = ExchangeNode.objects.all()
    serializer_class = ExchangeNodeSerializer
    permission_classes = [IsAdminUser]


class NewOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = Order.objects.create()
        order.contractor = request.user.contractor
        if request.user.contractor is not None:
            order.partner = request.user.contractor.partner

        if IsDeepDebug:
            print_to(None, '\n%s\nNewOrderView.post[request.data], contractor:%s' % ('-' * 20, order.contractor))
            for item in request.data:
                print_to(None, '\n%s' % str(item))

        for item in request.data:
            price_serializer = PriceSerializer(data=item)
            price_serializer.is_valid(raise_exception=True)
            data = price_serializer.validated_data

            if IsDeepDebug:
                print_to(None,
                         '\nNewOrderView.data:\n%s' % '\n'.join(['%s:%s' % (key, data[key]) for key in data.keys()]))

            OrdersDetail.objects.create(
                order=order,
                product=data["product"],
                characteristic=data["characteristic"],
                price=data["price"],
                quantity=data["count"],
                total=data["count"] * data["price"]
            )

        order.save()

        serializer = OrderSerializer(order)
        if IsDeepDebug:
            print_to(None, '\n%s' % ('-' * 20))

        return general_response(serializer.data, response_status=status.HTTP_201_CREATED)


def test_task(request):
    upload_orders.delay()
    return HttpResponse("<h1>Запуск задачи</h1>")
