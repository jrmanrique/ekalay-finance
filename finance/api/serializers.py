from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from finance.models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts


class CashInflowSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name = 'finance-api:inflow-edit',
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


class CashInflowEditSerializer(ModelSerializer):
    account_title_text = SerializerMethodField()

    class Meta:
        model = CashInflow
        fields = ['id', 'date', 'flow_type', 'ref_num', 'account_title', 'account_title_text', 'payor', 'amount', 'document', 'notes']
        read_only_fields = ['id', 'flow_type', 'ref_num']

    def get_account_title_text(self, object):
        return object.account_title.account_title

