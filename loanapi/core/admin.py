from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from .models import Loan, Payment
# Register your models here.


TokenAdmin.raw_id_fields = ['user']
admin.site.register(Loan)
admin.site.register(Payment)

