from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Account(models.Model):
    EURO_ = 'EUR'
    US_DOLLAR = 'USD'
    IRANIAN_RIAL = 'IRR'

    CURRENCY_CHOICE = [
        (EURO_, 'euro'),
        (US_DOLLAR, 'U.S. dollar'),
        (IRANIAN_RIAL, 'Iranian Rial')
    ]

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.PositiveBigIntegerField(default=0)
    currency = models.CharField(
        choices=CURRENCY_CHOICE, max_length=3, default=IRANIAN_RIAL)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.owner


class Transfer(models.Model):
    from_account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='transfers_from', verbose_name="from client")
    to_account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='transfers_to', verbose_name='to client')
    amount = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)


class Entry(models.Model):
    account_id = models.ForeignKey(
        Account, models.CASCADE, related_name='enteries', verbose_name='client name')
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
