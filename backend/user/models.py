from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from catalog.models import Contractor


class CustomUser(AbstractUser):
    __PASSWORD_LENGTH__: int = 8

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    contractor = models.OneToOneField(
        Contractor,
        on_delete=models.PROTECT,
        verbose_name='Контрагент',
        related_name='contractor_profile',
        default=None,
        null=True,
        blank=True
    )
    full_name = models.CharField(
        verbose_name="Наименование полное",
        max_length=254,
        null=True,
        blank=True
    )

    def generate_random_password(self):
        return BaseUserManager.make_random_password(self.__PASSWORD_LENGTH__)

    def send_welcome_email(self, password):
        subject = "Регистрация в личном кабинете [название сайта]."
        html_message = render_to_string('user/email_welcome.html', {
            'user': self,
            'domain': 'localhost',
            'password': password
        })
        from_email = 'admin <test1c@atomatix.ru>'
        to_email = self.email
        email = EmailMessage(subject, html_message, from_email, [to_email])
        email.content_subtype = 'html'
        email.send()

    def __str__(self):
        return f'{self.full_name} ({self.username})'

