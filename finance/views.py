from decimal import *

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CashInflowForm, CashOutflowForm, ChartOfAccountsForm
from .functions import *
from .models import CashInflow, CashOutflow, ChartOfAccounts, AccountTypes


def index(request):
    num = 32
    balance = 124795.70
    context = {
        'all_inflows' : CashInflow.objects.all(),
        'all_outflows' : CashOutflow.objects.all(),
        'all_accounts' : ChartOfAccounts.objects.all(),
        'all_account_types' : AccountTypes.objects.all(),
        'total_inflow' : sumFlow(CashInflow),
        'total_outflow' : sumFlow(CashOutflow),
        'title' : getField(num),
        'total_title' : sumTitle(getField(num)),
        'type' : getType(num),
        'total_type' : sumType(getType(num)),
        'list_accounts' : listAccounts(),
        'list_types' : listTypes(),
        'balance' : Decimal(balance).quantize(Decimal('.01')),
        'test' : testLols(num),
    }
    return render(request, 'finance/index.html', context)


def inflows(request):
    all_inflows = CashInflow.objects.all()
    context = {
        'all_inflows' : all_inflows,
    }
    return render(request, 'finance/inflows.html', context)


''' def inflowCreate(request):
    if request.method == "POST":
        form = CashInflowForm(request.POST)
        if form.is_valid():
            inflow = form.save(commit=False)
            inflow.save()
    else:
        form = CashInflowForm()
    return render(request, 'finance/inflow-form.html', {'form': form}) '''


class InflowCreate(CreateView):
    form_class = CashInflowForm
    template_name = 'finance/generic-form.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "This transaction has been recorded.")
        return render(self.request, 'finance/generic-form.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(InflowCreate, self).get_context_data(**kwargs)
        form = self.form_class()
        pageTitle = 'Add Cash Inflow'
        context = {
            'form' : form,
            'pageTitle' : pageTitle,
        }
        return context


''' def inflowEdit(request, pk):
    inflow = get_object_or_404(CashInflow, pk=pk)
    if request.method == "POST":
        form = CashInflowForm(request.POST, instance=inflow)
        if form.is_valid():
            inflow = form.save(commit=False)
            inflow.save()
            # return redirect('inflowEdit', pk=inflow.pk)
            return redirect('index')
    else:
        form = CashInflowForm(instance=inflow)
    return render(request, 'finance/inflow-form.html', {'form': form}) '''


class InflowEdit(UpdateView):
    model = CashInflow
    form_class = CashInflowForm
    template_name = 'finance/generic-form.html'

    def get(self, request, **kwargs):
        self.object = self.model.objects.get(pk=self.kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        inflow = self.model.objects.get(pk=self.kwargs['pk'])
        return inflow

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "The transaction has been updated.")
        return redirect('index')
        # return render(self.request, 'finance/generic-form.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(InflowEdit, self).get_context_data(**kwargs)
        form = self.form_class(instance=self.get_object(self))
        pageTitle = 'Edit Cash Inflow'
        context = {
            'form' : form,
            'pageTitle' : pageTitle,
        }
        return context


''' def inflowDelete(request, pk):
    inflow = get_object_or_404(CashInflow, pk=pk)
    inflow.delete()
    # outflows = outflow.objects.filter(user=request.user)
    return redirect('index') '''


class InflowDelete(DeleteView):
    model = CashInflow
    template_name = 'finance/delete-template.html'
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "The transaction has been deleted successfully.")
        return super(InflowDelete,self).delete(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        inflow = self.model.objects.get(pk=self.kwargs['pk'])
        return inflow
        
    def get_context_data(self, **kwargs):
        context = super(InflowDelete, self).get_context_data(**kwargs)
        texta = 'Inflow'
        textb = texta.lower()
        context = {
            'texta' : texta,
            'textb' : textb,
            'textc' : self.get_object(self),
        }
        return context


def outflows(request):
    all_outflows = CashOutflow.objects.all()
    context = {
        'all_outflows' : all_outflows,
    }
    return render(request, 'finance/outflows.html', context)


class OutflowCreate(CreateView):
    form_class = CashOutflowForm
    template_name = 'finance/generic-form.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "This transaction has been recorded.")
        return render(self.request, 'finance/generic-form.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(OutflowCreate, self).get_context_data(**kwargs)
        form = self.form_class()
        pageTitle = 'Add Cash Outflow'
        context = {
            'form' : form,
            'pageTitle' : pageTitle,
        }
        return context
        

class OutflowEdit(UpdateView):
    model = CashOutflow
    form_class = CashOutflowForm
    template_name = 'finance/generic-form.html'

    def get(self, request, **kwargs):
        self.object = self.model.objects.get(pk=self.kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        outflow = self.model.objects.get(pk=self.kwargs['pk'])
        return outflow

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "The transaction has been updated.")
        return redirect('index')
        # return render(self.request, 'finance/generic-form.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(OutflowEdit, self).get_context_data(**kwargs)
        form = self.form_class(instance=self.get_object(self))
        pageTitle = 'Edit Cash Outflow'
        context = {
            'form' : form,
            'pageTitle' : pageTitle,
        }
        return context


class OutflowDelete(DeleteView):
    model = CashOutflow
    template_name = 'finance/delete-template.html'
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "The transaction has been deleted successfully.")
        return super(OutflowDelete,self).delete(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        outflow = self.model.objects.get(pk=self.kwargs['pk'])
        return outflow
        
    def get_context_data(self, **kwargs):
        context = super(OutflowDelete, self).get_context_data(**kwargs)
        texta = 'Outflow'
        textb = texta.lower()
        context = {
            'texta' : texta,
            'textb' : textb,
            'textc' : self.get_object(self),
        }
        return context


class AccountCreate(CreateView):
    form_class = ChartOfAccountsForm
    template_name = 'finance/generic-form.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "This account has been added.")
        return render(self.request, 'finance/generic-form.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(AccountCreate, self).get_context_data(**kwargs)
        form = self.form_class()
        pageTitle = 'Add Account'
        context = {
            'form' : form,
            'pageTitle' : pageTitle,
        }
        return context


class AccountEdit(UpdateView):
    model = ChartOfAccounts
    form_class = ChartOfAccountsForm
    template_name = 'finance/generic-form.html'

    def get(self, request, **kwargs):
        self.object = self.model.objects.get(pk=self.kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        account = self.model.objects.get(pk=self.kwargs['pk'])
        return account

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "The account has been updated.")
        return redirect('index')
        # return render(self.request, 'finance/generic-form.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(AccountEdit, self).get_context_data(**kwargs)
        form = self.form_class(instance=self.get_object(self))
        pageTitle = 'Edit Account'
        context = {
            'form' : form,
            'pageTitle' : pageTitle,
        }
        return context

    
class AccountDelete(DeleteView):
    model = ChartOfAccounts
    template_name = 'finance/delete-template.html'
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "The account has been deleted successfully.")
        return super(AccountDelete, self).delete(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        account = self.model.objects.get(pk=self.kwargs['pk'])
        return account
        
    def get_context_data(self, **kwargs):
        context = super(AccountDelete, self).get_context_data(**kwargs)
        texta = 'Account'
        textb = texta.lower()
        context = {
            'texta' : texta,
            'textb' : textb,
            'textc' : self.get_object(self),
        }
        return context
