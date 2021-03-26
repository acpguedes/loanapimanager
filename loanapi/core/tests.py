from easy_test.cases.test_model import ModelTest

from .models import Loan, Payment


class LoanModelTest(ModelTest):
    class Meta:
        obj = Loan()


class PaymentModelTest(ModelTest):
    class Meta:
        obj = Payment()
