from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from finance.models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts


class CashInflowSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name = 'finance-api:inflow-detail',
        lookup_field = 'pk',
    )
    account_title = SerializerMethodField()

    class Meta:
        model = CashInflow
        fields = ['url', 'id', 'date', 'flow_type', 'ref_num', 'account_title', 'payor', 'amount', 'document', 'notes']

    def get_account_title(self, object):
        return object.account_title.account_title


class CashInflowCreateSerializer(ModelSerializer):

    class Meta:
        model = CashInflow
        fields = ['date', 'account_title', 'payor', 'amount', 'document', 'notes']
