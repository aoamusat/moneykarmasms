from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

# Create your models here.


class Account(AbstractUser):
    pass


class PhoneNumber(models.Model):
    number = models.CharField(max_length=15, null=True, blank=True)
    account = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, verbose_name="Account ID"
    )

    class Meta:
        ordering = ("account",)

    def __str__(self) -> str:
        return "{} => {}".format(self.account.username, self.number)


class Message(models.Model):
    frm = models.CharField(
        verbose_name="From",
        max_length=16,
        null=False,
        validators=[MinLengthValidator(limit_value=6)],
    )
    to = models.CharField(
        verbose_name="To",
        max_length=16,
        null=False,
        validators=[MinLengthValidator(limit_value=6)],
    )
    text = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(limit_value=1)],
        null=False,
    )
