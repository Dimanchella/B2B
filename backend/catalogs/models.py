from django.contrib.auth import get_user_model
from django.db import models
from uuid import uuid4


class ProductsGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(verbose_name="Наименование", max_length=256)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Родитель",
        related_name="group"
    )

    def __str__(self):
        return f"{self.title} - {self.parent}"

    class Meta:
        verbose_name = 'Группа номенклатуры'
        verbose_name_plural = 'Группы номенклатуры'


class UseCharacteristic(models.TextChoices):
    NOT_USE = 'NU', 'Не используется'
    GENERAL_SELF_TYPE = 'GST', 'Общие для вида номенклатуры'
    GENERAL_OTHER_TYPE = 'GOT', 'Общие с другим видом номенклатуры'
    INDIVIDUAL = 'IND', 'Индивидуальные для номенклатуры'


class TypeOfProducts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид номенклатуры'
        verbose_name_plural = 'Виды номенклатуры'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    full_name = models.CharField(verbose_name="Наименование полное", max_length=256)
    group = models.ForeignKey(
        ProductsGroup,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Группа",
        related_name="products"
    )
    use_characteristic = models.CharField(
        verbose_name="Варианты использования характеристик",
        choices=UseCharacteristic.choices,
        max_length=64,
        default=UseCharacteristic.NOT_USE
    )
    type_of_product = models.ForeignKey(
        TypeOfProducts,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Вид номенклатуры',
        related_name='type_of_product'
    )
    description = models.TextField(verbose_name='Описание', max_length=2048, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатура'


def image_dir_path(instance, filename):
    return 'products_images/{}/{}'.format(instance.product.id, filename)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Номенклатура',
        related_name='product_images'
    )
    image = models.ImageField(verbose_name='Изображение', upload_to=image_dir_path, default=None)

    def __str__(self):
        return f"{self.product} - {self.image}"

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Characteristic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=256)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Номенклатура',
        related_name='product_characteristic'
    )
    type_of_products = models.ForeignKey(
        TypeOfProducts,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Вид номенклатуры',
        related_name='type_of_products_characteristic'
    )

    def __str__(self):
        return f"{self.name} ({self.product}/{self.type_of_products})"

    class Meta:
        verbose_name = 'Характеристика номенклатуры'
        verbose_name_plural = 'Характеристики номенклатуры'


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Partner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(
        verbose_name="Наименование",
        max_length=254,
        null=True,
        blank=True
    )
    full_name = models.CharField(
        verbose_name="Наименование полное",
        max_length=254,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.full_name})"

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'


class TypeOfContractors(models.TextChoices):
    COMPANY = 'COM', 'Юридическое лицо'
    PERSON = 'PER', 'Физическое лицо'
    OUTER_COMPANY = 'OCOM', 'Юридическое лицо не резидент'
    INDIVIDUAL = 'IND', 'Индивидуальный предприниматель'


class Contractor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    partner = models.ForeignKey(
        Partner,
        on_delete=models.DO_NOTHING,
        verbose_name='Партнер',
        default=None,
        related_name='contractor',
        null=True,
        blank=True
    )
    name = models.CharField(verbose_name="Наименование", max_length=256, unique=True)
    full_name = models.CharField(
        verbose_name="Сокращенное юр. наименование",
        max_length=256,
        blank=True
    )
    status = models.CharField(
        verbose_name="Юр/Физлицо",
        max_length=100,
        choices=TypeOfContractors.choices,
        default=TypeOfContractors.COMPANY,
        blank=True,
    )
    inn = models.CharField(verbose_name="ИНН", max_length=16)
    kpp = models.CharField(verbose_name="КПП", max_length=16, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.full_name} {self.inn}/{self.kpp}"

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class Agreement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=264)
    number = models.CharField(verbose_name="Номер", max_length=128)
    date = models.DateField(verbose_name="Дата")
    partner = models.ForeignKey(
        Partner,
        on_delete=models.PROTECT,
        verbose_name='Партнер',
        default=None,
        related_name='partner_agreement',
        null=True,
        blank=True
    )
    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.PROTECT,
        verbose_name='Контрагент',
        default=None,
        related_name='contractor_agreement',
        null=True,
        blank=True
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        verbose_name='Организация',
        default=None,
        related_name='organization_agreement',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} №{self.number} от {self.date} - {self.contractor}"

    class Meta:
        verbose_name = 'Соглашение об условиях продаж'
        verbose_name_plural = 'Соглашения об условиях продаж'


class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=264)
    number = models.CharField(verbose_name="Номер", max_length=128)
    date = models.DateField(verbose_name="Дата")
    partner = models.ForeignKey(
        Partner,
        on_delete=models.PROTECT,
        verbose_name='Партнер',
        default=None,
        related_name='partner_contract'
    )
    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.PROTECT,
        verbose_name='Контрагент',
        default=None,
        related_name='contractor_contract'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        verbose_name='Организация',
        default=None,
        related_name='organization_contract'
    )
    default = models.BooleanField(verbose_name="Использовать по умолчанию", default=False)

    def __str__(self):
        return f"{self.name} №{self.number} от {self.date}"

    class Meta:
        verbose_name = 'Договор с контрагентом'
        verbose_name_plural = 'Договора с контрагентами'
