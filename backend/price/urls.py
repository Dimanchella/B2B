from django.urls import path, include
from .views import PriceViewSet, ProductDetailViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# Операции с Прайс-листом
router.register(r'backend/api/v1/prices', PriceViewSet, basename='prices')

urlpatterns = [
    path('', include(router.urls)),
    path('backend/api/v1/price_detail/', ProductDetailViewSet.as_view(), name='price_detail')
]
