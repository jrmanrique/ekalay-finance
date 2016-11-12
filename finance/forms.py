from datetime import datetime

from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Fieldset, Layout, Reset, Submit
from django import forms

from . import functions
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


class StatementForm(forms.Form):
    from_date = forms.DateField(initial=functions.from_date, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(initial=functions.to_date, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(StatementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_action = 'statement'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.label_class = 'col-lg-0'
        self.helper.field_class = 'col-lg-12'
        self.helper.layout = Layout(
            Fieldset(
                '',
                PrependedText('from_date', 'From'),
                PrependedText('to_date', 'To'),
            ),
            FormActions(
                Submit('', 'Filter', css_class='btn btn-success'),
                Reset('reset', 'Reset', css_class="btn btn-default"),
                HTML("<button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Close</button>"),
            )
        )
