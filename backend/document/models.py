from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from uuid import uuid4

from catalog.models import (
    Contractor,
    Organization,
    Partner,
    Agreement,
    Contract,
    Product,
    Characteristic,
)


class SiteOrderStatus(models.TextChoices):
    CREATED = "CR", "Создан"
    WRITEN = "WR", "В обработке"
    PROCESSED = "PR", "Обработан"
    CLOSED = "CL", "Закрыт"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date_time = models.DateTimeField(verbose_name="Дата и время", default=timezone.now)
    number = models.CharField(
        verbose_name="Номер",
        max_length=64,
        default='',
        blank=True,
        null=True
    )
    partner = models.ForeignKey(
        Partner,
        on_delete=models.PROTECT,
        verbose_name="Партнер",
        related_name="partner_order",
        default=None,
        blank=True,
        null=True
    )
    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.PROTECT,
        verbose_name="Контрагент",
        related_name="contractor_order",
        default=None,
        blank=True,
        null=True
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        verbose_name="Организация",
        related_name="organization_order",
        default=None,
        blank=True,
        null=True
    )
    agreement = models.ForeignKey(
        Agreement,
        on_delete=models.PROTECT,
        verbose_name="Соглашение",
        related_name="agreement_order",
        default=None,
        null=True,
        blank=True
    )
    contract = models.ForeignKey(
        Contract,
        on_delete=models.PROTECT,
        verbose_name="Договор",
        related_name="contract_order",
        default=None,
        null=True,
        blank=True
    )
    site_status = models.CharField(
        verbose_name="Статус заказа на сайте",
        max_length=10,
        choices=SiteOrderStatus.choices,
        default=SiteOrderStatus.CREATED
    )

    def __str__(self):
        return f"Заказ клиента №{self.number} от {self.date_time.date()} - {self.partner}"

    def fix_exchange(self):
        exchange = ExchangeNode.objects.filter(order=self)
        if exchange:
            exchange_obj = exchange.get()
        else:
            exchange_obj = ExchangeNode()
        exchange_obj.order = self
        exchange_obj.updated_at = timezone.localtime(timezone.now())
        exchange_obj.save()

    class Meta:
        verbose_name = "Заказ клиента"
        verbose_name_plural = "Заказы клиентов"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ клиента",
        related_name="order_orders_detail",
        default=None
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Номенклатура",
        related_name="product_orders_detail",
        default=None
    )
    characteristic = models.ForeignKey(
        Characteristic,
        on_delete=models.PROTECT,
        verbose_name="Характеристика",
        related_name="product_characteristic",
        default=None,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Цена"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        verbose_name="Количество"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Сумма"
    )

    def __str__(self):
        return f'Заказ клиента №{self.order.number} от {self.order.date_time.date()} - {self.product}'

    class Meta:
        verbose_name = "Заказ клиента (Товары)"
        verbose_name_plural = "Заказы клиентов (Товары)"


class ExchangeNode(models.Model):
    updated_at = models.DateTimeField(verbose_name="Дата и время изменения", default=timezone.now)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ клиента",
        default=None,
        related_name="order_exchange_node"
    )

    def __str__(self):
        return f"({self.updated_at}) {self.order}"

    class Meta:
        verbose_name = "Измененный заказ"
        verbose_name_plural = "Измененные заказы"

