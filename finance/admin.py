from django.contrib import admin

from .models import CashInflow, CashOutflow, ChartOfAccounts, AccountTypes

# Register your models here.

admin.site.register(CashInflow)
admin.site.register(CashOutflow)
admin.site.register(ChartOfAccounts)
admin.site.register(AccountTypes)
