from django import forms

from .models import CashInflow, CashOutflow, ChartOfAccounts


class CashInflowForm(forms.ModelForm):

    class Meta:
        model = CashInflow
        fields = ['date', 'account_title', 'payor', 'amount', 'document', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'account_title': forms.Select(attrs={'class': 'form-control'}),
            'payor': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'document': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


class CashOutflowForm(forms.ModelForm):

    class Meta:
        model = CashOutflow
        fields = ['date', 'account_title', 'payee', 'purpose', 'amount', 'document', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'account_title': forms.Select(attrs={'class': 'form-control'}),
            'payee': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'document': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


class ChartOfAccountsForm(forms.ModelForm):

    class Meta:
        model = ChartOfAccounts
        fields = ['ref_num', 'account_title', 'account_type']
        widgets = {
            'ref_num': forms.NumberInput(attrs={'class': 'form-control'}),
            'account_title': forms.TextInput(attrs={'class': 'form-control'}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
        }
