from calendar import monthrange, month_name

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CashInflowForm, CashOutflowForm, ChartOfAccountsForm
from .methods import *
from .models import CashInflow, CashOutflow, ChartOfAccounts, AccountTypes


def index(request):
    context = {
        'all_inflows' : CashInflow.objects.all(),
        'all_outflows' : CashOutflow.objects.all(),
        'all_accounts' : ChartOfAccounts.objects.all(),
        'all_account_types' : AccountTypes.objects.all(),
        'total_inflow' : sumFlow(CashInflow, monthed),
        'total_outflow' : sumFlow(CashOutflow, monthed),
        'title' : getField(num),
        'total_title' : sumRefnumNet(num),
        'type' : getType(num),
        'total_type' : sumTypeNet(getType(num)),
        'list_accounts' : listAccounts(),
        'list_types' : listTypes(),
        'balance' : Decimal(balance).quantize(Decimal('.01')),
        'beg_of_month' : str(1) + ' ' + month_name[now.month] + ' ' + str(now.year),
        'end_of_month' : str(monthrange(now.year, now.month)[1]) + ' ' + month_name[now.month] + ' ' + str(now.year),
        'test' : CashOutflow.objects.filter(date__month=now.month).aggregate(Sum('amount'))
    }
    return render(request, 'finance/view.html', context)


def view(request):
    context = {
        'all_inflows' : CashInflow.objects.all(),
        'all_outflows' : CashOutflow.objects.all(),
        'all_accounts' : ChartOfAccounts.objects.all(),
        'total_inflow' : sumFlow(CashInflow, monthed),
        'total_outflow' : sumFlow(CashOutflow, monthed),
        'title' : getField(num),
        'total_title' : sumRefnumNet(num, monthed),
        'type' : getType(num),
        'total_type' : sumTypeNet(getType(num), monthed),
        'test' : str(sumRefnumInflow(num, monthed)) + ' - ' + str(sumRefnumOutflow(num, monthed)),
    }
    return render(request, 'finance/view.html', context)


def statement(request):
    context = {
        'all_inflows' : CashInflow.objects.all(),
        'all_outflows' : CashOutflow.objects.all(),
        'all_accounts' : ChartOfAccounts.objects.all(),
        'all_account_types' : AccountTypes.objects.all(),
        'total_inflow' : sumFlow(CashInflow, monthed),
        'total_outflow' : sumFlow(CashOutflow, monthed),
        'list_accounts' : listAccounts(),
        'list_types' : listTypes(),
        'balance' : Decimal(balance).quantize(Decimal('.01')),
        'beg_of_month' : str(1) + ' ' + month_name[now.month] + ' ' + str(now.year),
        'end_of_month' : str(monthrange(now.year, now.month)[1]) + ' ' + month_name[now.month] + ' ' + str(now.year),
    }
    return render(request, 'finance/statement.html', context)


def finAdmin(request):
    messages.warning(request, "Make sure you know what you are doing.")
    if request.method == "POST":
        form = ChartOfAccountsForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
            messages.success(request, "This account has been added.")
    else:
        form = ChartOfAccountsForm()
    context = {
        'form' : form,
        'all_accounts' : ChartOfAccounts.objects.all(),
        'all_account_types' : AccountTypes.objects.all(),
        'back' : 'finadmin',
    }
    return render(request, 'finance/fin-admin.html', context)


class FinAdminEdit(UpdateView):
    edit_mode = True
    model = ChartOfAccounts
    form_class = ChartOfAccountsForm
    template_name = 'finance/fin-admin.html'

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
        return redirect('finadmin')
        # return render(self.request, 'finance/generic-form.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(FinAdminEdit, self).get_context_data(**kwargs)
        form = self.form_class(instance=self.get_object(self))
        context = {
            'form' : form,
            'edit_mode' : self.edit_mode,
            'back' : 'finadmin',
        }
        return context

    
class FinAdminDelete(DeleteView):
    delete_mode = True
    model = ChartOfAccounts
    template_name = 'finance/fin-admin.html'
    success_url = reverse_lazy('finadmin')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "The account has been deleted successfully.")
        return super(FinAdminDelete,self).delete(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        account = self.model.objects.get(pk=self.kwargs['pk'])
        return account
        
    def get_context_data(self, **kwargs):
        context = super(FinAdminDelete, self).get_context_data(**kwargs)
        texta = 'Account'
        textb = texta.lower()
        context = {
            'texta' : texta,
            'textb' : textb,
            'textc' : self.get_object(self),
            'delete_mode' : self.delete_mode,
            'back' : 'finadmin',
        }
        return context
    
    
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
