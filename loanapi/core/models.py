from django.db import models
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


def random_string_generator(n=32):
    return get_random_string(n)


class Loan(models.Model):
    LoanID = models.CharField(
        default=random_string_generator,
        primary_key=True,
        unique=True,
        max_length=32
    )
    LoanNominalValue = models.DecimalField(decimal_places=2, max_digits=10)
    MonthlyFees = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    ipAddress = models.GenericIPAddressField()
    LoanRequestDay = models.DateField()
    Bank = models.TextField()
    ClientIDRef = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.LoanID


class Payment(models.Model):
    PaymentValue = models.DecimalField(decimal_places=2, max_digits=10)
    PaymentDay = models.DateField()
    LoanIDRef = models.ForeignKey(Loan, on_delete=models.CASCADE)
    ClientIDRef = Loan.ClientIDRef

    objects = models.Manager()
