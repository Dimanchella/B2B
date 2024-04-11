from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, ExchangeNodeViewSet, test_task, NewOrderView

router = DefaultRouter()
# Операции с заказами
router.register(r'backend/api/v1/orders', OrderViewSet, basename='orders')
# Обмен заказами с 1С
router.register(r'backend/api/v1/exchanges', ExchangeNodeViewSet, basename='exchanges')


urlpatterns = [
    path('', include(router.urls)),
    path('backend/test_task/', test_task, name='test_task'),
    path('backend/api/v1/create_new_order/', NewOrderView.as_view(), name='create_new_order')
]
