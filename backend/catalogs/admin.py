from django.contrib import admin
from .models import (
    TypeOfProducts,
    Product,
    ProductsGroup,
    Image,
    Characteristic,
    Organization,
    Partner,
    Contractor,
    Agreement,
    Contract
)

admin.site.register(TypeOfProducts)
admin.site.register(Product)
admin.site.register(ProductsGroup)
admin.site.register(Image)
admin.site.register(Characteristic)
admin.site.register(Organization)
admin.site.register(Partner)
admin.site.register(Contractor)
admin.site.register(Agreement)
admin.site.register(Contract)
