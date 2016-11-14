from django.contrib import admin

from .models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts


admin.site.register(CashInflow)
admin.site.register(CashOutflow)
admin.site.register(ChartOfAccounts)
admin.site.register(AccountTypes)
