from rest_framework.serializers import ModelSerializer

from finance.models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts


class CashInflowSerializer(ModelSerializer):

    class Meta:
        model = CashInflow
        fields = ['id', 'date', 'flow_type', 'ref_num', 'account_title', 'payor', 'amount', 'document', 'notes']


class CashInflowCreateSerializer(ModelSerializer):

    class Meta:
        model = CashInflow
        fields = ['date', 'ref_num', 'payor', 'amount', 'document', 'notes']
