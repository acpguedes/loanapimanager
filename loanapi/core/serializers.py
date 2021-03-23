from rest_framework.serializers import ModelSerializer

from .models import Loan, Payment


class LoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            'LoanID',
            'LoanNominalValue',
            'MonthlyFees',
            'LoanRequestDay',
            'Bank',
            'ipAddress'
        )


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'PaymentValue',
            'PaymentDay',
            'LoanIDRef',
            'ClientIDRef'
        )

