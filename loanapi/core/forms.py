from crispy_forms.helper import FormHelper
from django import forms
from django.forms import ModelForm

from .models import Loan, Payment


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        exclude = ['ClientIDRef']

    LoanNominalValue = forms.FloatField()
    MonthlyFees = forms.FloatField(max_value=100, min_value=0)
    IOF = forms.FloatField(max_value=100, min_value=0)
    ipAddress = forms.GenericIPAddressField()
    LoanRequestDay = forms.DateField()
    Bank = forms.TextInput
    helper = FormHelper()


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    PaymentValue = forms.FloatField()
    PaymentDay = forms.DateField()
