from django.contrib import admin
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

admin.site.register(TypeOfProduct)
admin.site.register(Product)
admin.site.register(ProductGroup)
admin.site.register(Image)
admin.site.register(Characteristic)
admin.site.register(Organization)
admin.site.register(Partner)
admin.site.register(Contractor)
admin.site.register(Agreement)
admin.site.register(Contract)

