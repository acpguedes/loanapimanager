from datetime import datetime, timedelta

from django.db.models import Sum

from .models import Loan, Payment


class LoanCalc:
    '''Class to calculate pro rata die and remaining remaining amount'''

    def __init__(self, user, loan_id):
        zero = datetime.min.time()
        self.today = datetime.combine(datetime.today(), zero)
        self.Loan = Loan.objects.filter(
            ClientIDRef=user
        ).get(
            LoanID=loan_id
        )
        self.Payment = Payment.objects.filter(
            LoanIDRef=loan_id
        ).aggregate(Sum('PaymentValue'))['PaymentValue__sum']
        self.fees = getattr(self.Loan, 'MonthlyFees')
        self.first_day = datetime.combine(
            getattr(self.Loan, 'LoanRequestDay'),
            zero
        )
        self.nominal_value = getattr(self.Loan, 'LoanNominalValue')

    def diff_days(self):
        return self.today - self.first_day

    def diff_months(self):
        num_months = (self.today.year - self.first_day.year) * 12 + (self.today.month - self.first_day.month)
        return num_months

    def last_day_of_month(self):
        if self.today.month == 12:
            return self.today.replace(day=31)
        return self.today.replace(month=self.today.month + 1, day=1) - timedelta(days=1)

    def remaining_days(self):
        return self.last_day_of_month().day - self.today.day

    def pro_rata_die(self):
        return self.fees / 100 / self.remaining_days()

    def compound_interest(self):
        amount = float(self.nominal_value) * (1 + self.fees / 100) ** self.diff_months()
        return float("{:.2f}".format(amount))

    def remaining_amount(self):
        return self.compound_interest() - float(self.Payment)
