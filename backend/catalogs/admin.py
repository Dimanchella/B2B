from django.contrib import admin
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

admin.site.register(TypesOfProducts)
admin.site.register(Products)
admin.site.register(ProductsGroup)
admin.site.register(Images)
admin.site.register(Characteristics)
admin.site.register(Organizations)
admin.site.register(Partners)
admin.site.register(Contractors)
admin.site.register(Agreements)
admin.site.register(Contracts)
