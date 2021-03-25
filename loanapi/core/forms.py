from crispy_forms.helper import FormHelper
from django import forms
from django.forms import ModelForm

from .models import Loan, Payment


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        exclude = ['ClientIDRef', 'ipAddress']

    LoanNominalValue = forms.FloatField()
    MonthlyFees = forms.FloatField(max_value=100, min_value=0)
    IOF = forms.FloatField(max_value=100, min_value=0)
    LoanRequestDay = forms.DateField()
    Bank = forms.TextInput
    helper = FormHelper()


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ['ClientIDRef']

    helper = FormHelper()

    def __init__(self, user, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['LoanIDRef'] = forms.ModelChoiceField(
            queryset=Loan.objects.filter(ClientIDRef=user)
        )
