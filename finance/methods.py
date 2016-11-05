from datetime import *
from decimal import *

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

from .models import CashInflow, CashOutflow, ChartOfAccounts, AccountTypes


# Global Variables


now = datetime.now() # Do not change. Currently unused.
monthed = False
test_mode = False

month = 10
num = 32
balance = 124795.70
in_bank = 99510.20


# Methods


def toggleMonthedMethod():
    " Toggle state of boolean monthed "
    global monthed
    monthed = not monthed
    return monthed


def convertNone(value):
    " Convert Nonetype to 0 "
    if value.get('amount__sum') is None:
        return Decimal(0).quantize(Decimal('.01'))
    else:
        return Decimal(value.get('amount__sum')).quantize(Decimal('.01'))


def getField(num, field='account_title'):
    " Get field from ref_num in models.ChartOfAccounts "
    try:
        field = ChartOfAccounts.objects.values().get(ref_num=num).get(field)
    except ObjectDoesNotExist:
        field = None
    return field


def getType(num):
    " Get account_type from ref_num in models.ChartOfAccounts "
    try:
        field_id = ChartOfAccounts.objects.values().get(ref_num=num).get('account_type_id')
        field = AccountTypes.objects.values().get(id=field_id).get('account_type')
    except ObjectDoesNotExist:
        field = None
    return field


def sumFlow(model, monthed=True):
    " Get sum of amount in model "
    if monthed:
        now = datetime.now()
        sum = model.objects.filter(date__month=month).aggregate(Sum('amount'))
    else:
        sum = model.objects.all().aggregate(Sum('amount'))
    return convertNone(sum)


def sumTypeInflow(account_type, monthed=True):
    " Get sum of amount of flow_type in models.CashInflow "
    if monthed:
        now = datetime.now()
        inflow = CashInflow.objects.filter(date__month=month, flow_type=account_type).aggregate(Sum('amount'))
    else:
        inflow = CashInflow.objects.filter(flow_type=account_type).aggregate(Sum('amount'))
    return convertNone(inflow)


def sumTypeOutflow(account_type, monthed=True):
    " Get sum of amount of flow_type in models.CashOutflow "
    if monthed:
        now = datetime.now()
        outflow = CashOutflow.objects.filter(date__month=month, flow_type=account_type).aggregate(Sum('amount'))
    else:
        outflow = CashOutflow.objects.filter(flow_type=account_type).aggregate(Sum('amount'))
    return convertNone(outflow)


def sumTypeNet(account_type, monthed):
    " Get sum of amount of flow_type in model "
    net_sum = sumTypeInflow(account_type, monthed)-sumTypeOutflow(account_type, monthed)
    return net_sum


def sumRefnumInflow(num, monthed=True):
    " Get sum of amount of ref_num in models.CashInflow "
    if monthed:
        now = datetime.now()
        inflow = CashInflow.objects.filter(date__month=month, ref_num=num).aggregate(Sum('amount'))
    else:
        inflow = CashInflow.objects.filter(ref_num=num).aggregate(Sum('amount'))
    return convertNone(inflow)


def sumRefnumOutflow(num, monthed=True):
    " Get sum of amount of ref_num in models.CashOutflow "
    if monthed:
        now = datetime.now()
        outflow = CashOutflow.objects.filter(date__month=month, ref_num=num).aggregate(Sum('amount'))
    else:
        outflow = CashOutflow.objects.filter(ref_num=num).aggregate(Sum('amount'))
    return convertNone(outflow)


def sumRefnumNet(num, monthed):
    " Get sum of amount of ref_num in model "
    sum = sumRefnumInflow(num, monthed)-sumRefnumOutflow(num, monthed)
    return sum


def listAccounts():
    " List accounts with respective balances "
    account_list = []
    for account in ChartOfAccounts.objects.order_by('ref_num'):
        account_details = {}
        account_details['num'] = account.ref_num
        account_details['title'] = account.account_title
        account_details['type'] = str(account.account_type)
        account_details['net'] = sumRefnumNet(account.ref_num, monthed)
        account_details['inflow'] = sumRefnumInflow(account.ref_num, monthed)
        account_details['outflow'] = sumRefnumOutflow(account.ref_num, monthed)
        account_list.append(account_details)
    return account_list


def listTypes():
    " List account_types with respective balances "
    type_list = []
    for account_type in AccountTypes.objects.all():
        type_details = {}
        type_details['type'] = account_type.account_type
        type_details['net'] = sumTypeNet(account_type, monthed)
        type_details['inflow'] = sumTypeInflow(account_type, monthed)
        type_details['outflow'] = sumTypeOutflow(account_type, monthed)
        type_list.append(type_details)
    return type_list


def testLols(num):
    " Test your shit "
    q = ChartOfAccounts.objects.filter(ref_num=num)
    return q
