from datetime import *
from decimal import *

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

from .models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts

# Global Variables


now = datetime.now() # Do not change. Currently unused.
monthed = False
test_mode = False

month = 11
num = 32
balance = 124795.70
in_bank = 99510.20


# Methods


def toggle_monthed():
    " Toggle state of boolean monthed "
    global monthed
    monthed = not monthed
    return monthed


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


def sum_flow(model):
    " Get sum of amount in model "
    if monthed:
        sum = model.objects.filter(date__month=month).aggregate(Sum('amount'))
    else:
        sum = model.objects.all().aggregate(Sum('amount'))
    return convert_none(sum)


def sum_type(model, account_type):
    " Get sum of amount of flow_type in model "
    if monthed:
        flow = model.objects.filter(date__month=month, flow_type=account_type).aggregate(Sum('amount'))
    else:
        flow = model.objects.filter(flow_type=account_type).aggregate(Sum('amount'))
    return convert_none(flow)


def sum_type_net(account_type):
    " Get net sum of amount of flow_type "
    net_sum = sum_type(CashInflow, account_type) - sum_type(CashOutflow,account_type)
    return net_sum


def sum_refnum(model, num):
    " Get sum of amount of ref_num in model "
    if monthed:
        flow = model.objects.filter(date__month=month, ref_num=num).aggregate(Sum('amount'))
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


def test_function(num):
    " Test your function "
    q = ChartOfAccounts.objects.filter(ref_num=num)
    return q
