from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, HTML, Layout, Reset, Submit

from django import forms
from django.core.urlresolvers import reverse

from .models import CashInflow, CashOutflow, ChartOfAccounts


class CashInflowForm(forms.ModelForm):

    class Meta:
        model = CashInflow
        fields = ['date', 'account_title', 'payor', 'amount', 'document', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'account_title': forms.Select(),
            'payor': forms.TextInput(),
            'amount': forms.NumberInput(),
            'document': forms.TextInput(),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(CashInflowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'date',
                'account_title',
                'payor',
                PrependedText('amount', 'PHP'),
                'document',
                'notes',
            ),
            FormActions(
                Submit('aform_pre', 'Submit', css_class='btn btn-success'),
                Reset('reset', 'Reset', css_class="btn btn-default"),
                HTML("<a class=\"btn btn-default\" href=\"{% url back %}\" role=\"button\">Back</a>"),
            )
        )


class CashOutflowForm(forms.ModelForm):

    class Meta:
        model = CashOutflow
        fields = ['date', 'account_title', 'payee', 'purpose', 'amount', 'document', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'account_title': forms.Select(),
            'payee': forms.TextInput(),
            'purpose': forms.TextInput(),
            'amount': forms.NumberInput(),
            'document': forms.TextInput(),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(CashOutflowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'date',
                'account_title',
                'payee',
                'purpose',
                PrependedText('amount', 'PHP'),
                'document',
                'notes',
            ),
            FormActions(
                Submit('bform_pre', 'Submit', css_class='btn btn-success'),
                Reset('reset', 'Reset', css_class="btn btn-default"),
                HTML("<a class=\"btn btn-default\" href=\"{% url back %}\" role=\"button\">Back</a>"),
            )
        )


class ChartOfAccountsForm(forms.ModelForm):

    class Meta:
        model = ChartOfAccounts
        fields = ['ref_num', 'account_title', 'account_type']
        widgets = {
            'ref_num': forms.NumberInput(),
            'account_title': forms.TextInput(),
            'account_type': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(ChartOfAccountsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'ref_num',
                'account_title',
                'account_type',
            ),
            FormActions(
                Submit('bform_pre', 'Submit', css_class='btn btn-success'),
                Reset('reset', 'Reset', css_class="btn btn-default"),
                HTML("<a class=\"btn btn-default\" href=\"{% url back %}\" role=\"button\">Back</a>"),
            )
        )
