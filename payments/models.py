from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models


class Bank(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        unique=True,
        error_messages={
            'unique': _("This name is already in use"),
        }
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Bank, self).save(*args, **kwargs)


class Company(AbstractUser):
    """
        Users within the Django authentication system are represented by this
        model.
        Username, password and email are required. Other fields are optional.
    """
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        unique=True,
        error_messages={
            'unique': _("This name is already in use"),
        }
    )

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        blank=False,
        null=False,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("This email is already in use"),
        }
    )
    is_email_subscribed = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, help_text=_('Defines if the company is active'))
    sign_up_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'is_staff', 'is_admin', 'is_active']

    class Meta:
        verbose_name = "Company"
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return '{name} - {email} - {sign_up_date}'.format(
            name=self.name,
            email=self.email,
            sign_up_date=self.sign_up_date
        )

    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)


class Account(models.Model):
    bss = models.PositiveSmallIntegerField(blank=False, null=False)
    account = models.PositiveIntegerField(blank=False, null=False)
    bank = models.ForeignKey(Bank, null=False, blank=False, on_delete=models.DO_NOTHING)

    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{bss} - {acc} - {bank}'.format(
            bss=self.bss,
            acc=self.account,
            bank=self.bank.name
        )

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)


class Payment(models.Model):
    STATUS_CREATED = 'C'
    STATUS_SUCCESSFUL = 'S'
    STATUS_FAILED = 'F'
    STATUS_DISPUTED = 'D'

    STATUS = (
        (STATUS_CREATED, 'Created'),
        (STATUS_SUCCESSFUL, 'Successful'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_DISPUTED, 'Disputed'),
    )

    status = models.CharField(max_length=1, blank=False, null=False, choices=STATUS, db_index=True)

    date_transaction = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    # FK
    company = models.ForeignKey(Company, null=False, blank=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '{company} - {date_transaction} - {status}'.format(
            company=self.company.name,
            date_transaction=self.date_transaction,
            status=self.status
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        super(Payment, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def clean(self):
        super().clean()
