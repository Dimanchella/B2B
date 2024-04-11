from django.urls import path, include
from .views import (
    TypeOfProductViewSet,
    ProductViewSet,
    ProductGroupViewSet,
    ProductGroupTree,
    ImageViewSet,
    CharacteristicViewSet,
    OrganizationViewSet,
    PartnerViewSet,
    ContractorViewSet,
    AgreementViewSet,
    ContractViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'backend/api/v1/types_of_products', TypeOfProductViewSet, basename='types_of_products')
router.register(r'backend/api/v1/products', ProductViewSet, basename='products')
router.register(r'backend/api/v1/products_groups', ProductGroupViewSet, basename='products_groups')
router.register(r'backend/api/v1/images', ImageViewSet, basename='images')
router.register(r'backend/api/v1/characteristics', CharacteristicViewSet, basename='characteristics')
router.register(r'backend/api/v1/organizations', OrganizationViewSet, basename='organizations')
router.register(r'backend/api/v1/partners', PartnerViewSet, basename='partners')
router.register(r'backend/api/v1/contractors', ContractorViewSet, basename='contractors')
router.register(r'backend/api/v1/agreements', AgreementViewSet, basename='agreements')
router.register(r'backend/api/v1/contracts', ContractViewSet, basename='contracts')

urlpatterns = [
    path('', include(router.urls)),
    path('backend/api/v1/products_groups_tree/', ProductGroupTree.as_view(), name='products_groups_tree')
]

