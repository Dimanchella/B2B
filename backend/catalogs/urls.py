from django.urls import path, include
from .views import (
    TypesOfProductsViewSet,
    ProductsViewSet,
    ProductsGroupViewSet,
    ProductsGroupTree,
    ImagesViewSet,
    CharacteristicsViewSet,
    OrganizationsViewSet,
    PartnersViewSet,
    ContractorsViewSet,
    AgreementsViewSet,
    ContractsViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'backend/api/v1/types_of_products', TypesOfProductsViewSet, basename='types_of_products')
router.register(r'backend/api/v1/products', ProductsViewSet, basename='products')
router.register(r'backend/api/v1/products_group', ProductsGroupViewSet, basename='products_group')
router.register(r'backend/api/v1/images', ImagesViewSet, basename='images')
router.register(r'backend/api/v1/characteristics', CharacteristicsViewSet, basename='characteristics')
router.register(r'backend/api/v1/organizations', OrganizationsViewSet, basename='organizations')
router.register(r'backend/api/v1/partners', PartnersViewSet, basename='partners')
router.register(r'backend/api/v1/contractors', ContractorsViewSet, basename='contractors')
router.register(r'backend/api/v1/agreements', AgreementsViewSet, basename='agreements')
router.register(r'backend/api/v1/contracts', ContractsViewSet, basename='contracts')

urlpatterns = [
    path('', include(router.urls)),
    path('backend/api/v1/products_group_tree/', ProductsGroupTree.as_view(), name='products_group_tree')
]
