from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.crypto import get_random_string


def random_string_generator(n=32):
    return get_random_string(n)


class Loan(models.Model):
    LoanID = models.CharField(
        default=random_string_generator,
        primary_key=True,
        unique=True,
        max_length=32,
        editable=False,
        null=False
    )
    LoanNominalValue = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    MonthlyFees = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    IOF = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    ipAddress = models.GenericIPAddressField(default='0.0.0.0')
    LoanRequestDay = models.DateField(default=datetime.now)
    Bank = models.TextField(default='')
    ClientIDRef = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.LoanID


class Payment(models.Model):
    PaymentValue = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    PaymentDay = models.DateField(
        default=datetime.now
    )
    LoanIDRef = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    objects = models.Manager()
