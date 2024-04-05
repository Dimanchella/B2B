from django.db import models
from catalogs.models import Product, Characteristic


class Price(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Номенклатура",
        related_name="product"
    )
    characteristic = models.ForeignKey(
        Characteristic,
        on_delete=models.PROTECT,
        verbose_name="Характеристика",
        default=None,
        blank=True,
        null=True,
        related_name="characteristic_price"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", blank=True, default=0)

    def __str__(self):
        return f"{self.product} ({self.characteristic}) - {self.price}"

    class Meta:
        verbose_name = 'Прайс'
        verbose_name_plural = 'Прайс'
