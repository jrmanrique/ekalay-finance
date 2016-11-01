from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

from .models import CashInflow, CashOutflow, ChartOfAccounts, AccountTypes


def convertNone(value):
    " Convert Nonetype to 0 "
    if value.get('amount__sum') is None:
        return 0
    else:
        return value.get('amount__sum')


def getField(num,field='account_title'):
    " Get field from ref_num in ChartOfAccounts "
    try:
        field = ChartOfAccounts.objects.values().get(ref_num=num).get(field)
    except ObjectDoesNotExist:
        field = None
    return field


def getType(num):
    " Get account_type from ref_num in ChartOfAccounts "
    try:
        field_id = ChartOfAccounts.objects.values().get(ref_num=num).get('account_type_id')
        field = AccountTypes.objects.values().get(id=field_id).get('account_type')
    except ObjectDoesNotExist:
        field = None
    return field


def sumFlow(model):
    " Get sum of amount in model "
    sum = model.objects.all().aggregate(Sum('amount')).get('amount__sum')
    return sum


def sumType(account_type):
    " Get sum of amount of flow_type in model "
    inflow = CashInflow.objects.filter(flow_type=account_type).aggregate(Sum('amount'))
    outflow = CashOutflow.objects.filter(flow_type=account_type).aggregate(Sum('amount'))
    sum = convertNone(inflow)-convertNone(outflow)
    return sum


def sumTitle(title):
    " Get sum of amount of account_title in model "
    inflow = CashInflow.objects.filter(account_title__account_title=title).aggregate(Sum('amount'))
    outflow = CashOutflow.objects.filter(account_title__account_title=title).aggregate(Sum('amount'))
    sum = convertNone(inflow)-convertNone(outflow)
    return sum


def sumRefnum(num):
    " Get sum of amount of ref_num in model "
    inflow = CashInflow.objects.filter(ref_num=num).aggregate(Sum('amount'))
    outflow = CashOutflow.objects.filter(ref_num=num).aggregate(Sum('amount'))
    sum = convertNone(inflow)-convertNone(outflow)
    return sum


def listAccounts():
    " List accounts with respective balances "
    account_list = []
    for account in ChartOfAccounts.objects.order_by('ref_num'):
        account_details = {}
        account_details['num'] = account.ref_num
        account_details['title'] = account.account_title
        account_details['type'] = str(account.account_type)
        account_details['value'] = sumRefnum(account.ref_num)
        account_list.append(account_details)
    return account_list


def listTypes():
    " List type with respective balances "
    type_list = []
    for account_type in AccountTypes.objects.all():
        type_details = {}
        type_details['type'] = account_type.account_type
        type_details['value'] = sumType(account_type)
        type_list.append(type_details)
    return type_list


def testLols(num):
    " Test your shit "
    q = ChartOfAccounts.objects.filter(ref_num=num)
    return q