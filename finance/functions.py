from datetime import datetime
from decimal import *

from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

from . import forms
from .models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts


# Global Variables


now = datetime.now()  # Defines current datetime. Do not change.
from_date = datetime.strftime(now, "%Y-%m-01")
to_date = datetime.strftime(now, "%Y-%m-%d")  # Default to_date if not set. Format: YYYY-MM-DD.
balance = 124795.70  # Starting balance from implementation (2016-10-01).

filtered = True  # If True, shows Statement data from from_date to to_date.
test_mode = False  # Shows test values in Summary tab.

num = 32
in_bank = 99510.20  # Currently not in use.


# Methods


def statement_filter(request):
    " Set filters for Statement "
    global from_date
    global to_date
    if request.method == "POST":
        form = forms.StatementForm(request.POST)
        from_date = form.data['from_date']
        to_date = form.data['to_date']
    else:
        form = forms.StatementForm()
    return form, from_date, to_date


def parse_date(iso_date):
    " Parse basic ISO 8601 date-only format into datetime.date format "
    if isinstance(iso_date, str):
        date_obj = datetime.strptime(iso_date, "%Y-%m-%d")
    else:
        date_obj = iso_date
    parsed_date = datetime.strftime(date_obj,"%d %B %Y")
    return parsed_date


def reload_database():
    " Reloads the database after modifying models.py "
    all_outflows = CashOutflow.objects.all()
    for outflow in all_outflows:
        outflow.save()
    all_inflows = CashInflow.objects.all()
    for inflow in all_inflows:
        inflow.save()
    return True


def is_super(user):
    " Check user access level "
    users_in_council = Group.objects.get(name="Council").user_set.all()
    users_in_finance = Group.objects.get(name="Finance").user_set.all()
    if user.is_superuser:
        access = True
    elif user in users_in_finance:
        access = False
    elif user in users_in_council:
        access = False
    else:
        access = False
    return access


def is_finance(user):
    " Check user access level "
    users_in_council = Group.objects.get(name="Council").user_set.all()
    users_in_finance = Group.objects.get(name="Finance").user_set.all()
    if user.is_superuser:
        access = True
    elif user in users_in_finance:
        access = True
    elif user in users_in_council:
        access = False
    else:
        access = False
    return access


def is_council(user):
    " Check user access level "
    users_in_council = Group.objects.get(name="Council").user_set.all()
    users_in_finance = Group.objects.get(name="Finance").user_set.all()
    if user.is_superuser:
        access = True
    elif user in users_in_finance:
        access = True
    elif user in users_in_council:
        access = True
    else:
        access = False
    return access


def convert_none(value):
    " Convert Nonetype to 0 "
    if value.get('amount__sum') is None:
        return Decimal(0).quantize(Decimal('.01'))
    else:
        return Decimal(value.get('amount__sum')).quantize(Decimal('.01'))


def get_field(num, field='account_title'):
    " Get field from ref_num in models.ChartOfAccounts "
    try:
        field = ChartOfAccounts.objects.values().get(ref_num=num).get(field)
    except ObjectDoesNotExist:
        field = None
    return field


def get_type(num):
    " Get account_type from ref_num in models.ChartOfAccounts "
    try:
        field_id = ChartOfAccounts.objects.values().get(ref_num=num).get('account_type_id')
        field = AccountTypes.objects.values().get(id=field_id).get('account_type')
    except ObjectDoesNotExist:
        field = None
    return field


def get_balance():
    " Get previous balance for filtering "
    prev_inflow = CashInflow.objects.filter(date__lt=from_date).aggregate(Sum('amount'))
    prev_outflow = CashOutflow.objects.filter(date__lt=from_date).aggregate(Sum('amount'))
    if filtered:
        filter_bal = Decimal(balance).quantize(Decimal('.01')) + convert_none(prev_inflow) - convert_none(prev_outflow)
    else:
        filter_bal = Decimal(balance).quantize(Decimal('.01'))
    return filter_bal


def sum_flow(model):
    " Get sum of amount in model "
    if filtered:
        sum = model.objects.exclude(date__gt=to_date).filter(date__gte=from_date).aggregate(Sum('amount'))
    else:
        sum = model.objects.all().aggregate(Sum('amount'))
    return convert_none(sum)


def sum_type(model, account_type):
    " Get sum of amount of flow_type in model "
    if filtered:
        flow = model.objects.exclude(date__gt=to_date).filter(date__gte=from_date, flow_type=account_type).aggregate(Sum('amount'))
    else:
        flow = model.objects.filter(flow_type=account_type).aggregate(Sum('amount'))
    return convert_none(flow)


def sum_type_net(account_type):
    " Get net sum of amount of flow_type "
    net_sum = sum_type(CashInflow, account_type) - sum_type(CashOutflow, account_type)
    return net_sum


def sum_refnum(model, num):
    " Get sum of amount of ref_num in model "
    if filtered:
        flow = model.objects.exclude(date__gt=to_date).filter(date__gte=from_date, ref_num=num).aggregate(Sum('amount'))
    else:
        flow = model.objects.filter(ref_num=num).aggregate(Sum('amount'))
    return convert_none(flow)


def sum_refnum_net(num):
    " Get net sum of amount of ref_num "
    sum = sum_refnum(CashInflow, num)-sum_refnum(CashOutflow, num)
    return sum


def list_accounts():
    " List accounts with respective balances "
    account_list = []
    for account in ChartOfAccounts.objects.order_by('ref_num'):
        account_details = {}
        account_details['num'] = account.ref_num
        account_details['title'] = account.account_title
        account_details['type'] = str(account.account_type)
        account_details['net'] = sum_refnum_net(account.ref_num)
        account_details['inflow'] = sum_refnum(CashInflow, account.ref_num)
        account_details['outflow'] = sum_refnum(CashOutflow, account.ref_num)
        account_list.append(account_details)
    return account_list


def list_types():
    " List account_types with respective balances "
    type_list = []
    for account_type in AccountTypes.objects.all():
        type_details = {}
        type_details['type'] = account_type.account_type
        type_details['net'] = sum_type_net(account_type)
        type_details['inflow'] = sum_type(CashInflow, account_type)
        type_details['outflow'] = sum_type(CashOutflow, account_type)
        type_list.append(type_details)
    return type_list


def test_function():
    " Test your function "
    prev_inflow = CashInflow.objects.filter(date__lte=from_date).aggregate(Sum('amount'))
    prev_outflow = CashOutflow.objects.filter(date__lte=from_date).aggregate(Sum('amount'))
    if filtered:
        filter_bal = Decimal(balance).quantize(Decimal('.01')) + convert_none(prev_inflow) - convert_none(prev_outflow)
    else:
        filter_bal = Decimal(balance).quantize(Decimal('.01'))
    return filter_bal
