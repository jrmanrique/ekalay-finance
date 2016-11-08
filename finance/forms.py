from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Fieldset, Layout, Reset, Submit
from django import forms

from .models import CashInflow, CashOutflow, ChartOfAccounts


class CashInflowForm(forms.ModelForm):

    class Meta:
        model = CashInflow
        fields = ['date', 'ref_num', 'payor', 'amount', 'document', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'ref_num': forms.Select(),
            'payor': forms.TextInput(),
            'amount': forms.NumberInput(),
            'document': forms.TextInput(),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(CashInflowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.fields['ref_num'].label = 'Account Title'

        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'date',
                'ref_num',
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
        fields = ['date', 'ref_num', 'payee', 'purpose', 'amount', 'document', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'ref_num': forms.Select(),
            'payee': forms.TextInput(),
            'purpose': forms.TextInput(),
            'amount': forms.NumberInput(),
            'document': forms.TextInput(),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(CashOutflowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.fields['ref_num'].label = 'Account Title'

        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'date',
                'ref_num',
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
