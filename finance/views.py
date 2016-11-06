from calendar import monthrange, month_name # Currently unused.

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CashInflowForm, CashOutflowForm, ChartOfAccountsForm
from .methods import *
from .models import CashInflow, CashOutflow, ChartOfAccounts, AccountTypes


def index(request):
    context = {
        'all_inflows': CashInflow.objects.all(),
        'all_outflows': CashOutflow.objects.all(),
        'all_accounts': ChartOfAccounts.objects.all(),
        'total_inflow': sumFlow(CashInflow, monthed),
        'total_outflow': sumFlow(CashOutflow, monthed),
        'title': getField(num),
        'total_title': sumRefnumNet(num, monthed),
        'type': getType(num),
        'total_type': sumTypeNet(getType(num), monthed),
        'balance': Decimal(balance).quantize(Decimal('.01')),
        'test_mode': test_mode,
        'test' : now,
    }
    return render(request, 'finance/index.html', context)


def statement(request):
    context = {
        'all_inflows': CashInflow.objects.all(),
        'all_outflows': CashOutflow.objects.all(),
        'all_accounts': ChartOfAccounts.objects.all(),
        'all_account_types': AccountTypes.objects.all(),
        'total_inflow': sumFlow(CashInflow, monthed),
        'total_outflow': sumFlow(CashOutflow, monthed),
        'list_accounts': listAccounts(),
        'list_types': listTypes(),
        'balance': Decimal(balance).quantize(Decimal('.01')),
        'in_bank': Decimal(in_bank).quantize(Decimal('.01')),
    }
    return render(request, 'finance/statement.html', context)


def toggleMonthed(request):
    toggleMonthedMethod()
    return redirect('statement')


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
        'form': form,
        'all_accounts': ChartOfAccounts.objects.all(),
        'all_account_types': AccountTypes.objects.all(),
        'back': 'finadmin',
    }
    return render(request, 'finance/fin-admin.html', context)


class FinAdmin(CreateView):
    form_class = ChartOfAccountsForm
    template_name = 'finance/fin-admin.html'

    def get(self, request, *args, **kwargs):
        messages.warning(self.request, "Make sure you know what you are doing.")
        return super(FinAdmin, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "This account has been created.")
        return render(self.request, 'finance/fin-admin.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(FinAdmin, self).get_context_data(**kwargs)
        form = self.form_class()
        context = {
            'form': form,
            'all_accounts': ChartOfAccounts.objects.all(),
            'all_account_types': AccountTypes.objects.all(),
            'back': 'finadmin',
        }
        return context


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
            'form': form,
            'edit_mode': self.edit_mode,
            'back': 'finadmin',
        }
        return context


class FinAdminDelete(DeleteView):
    edit_mode = True
    delete_mode = True
    form_class = ChartOfAccountsForm
    model = ChartOfAccounts
    template_name = 'finance/fin-admin.html'
    success_url = reverse_lazy('finadmin')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "The account has been deleted successfully.")
        return super(FinAdminDelete, self).delete(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        account = self.model.objects.get(pk=self.kwargs['pk'])
        return account

    def get_context_data(self, **kwargs):
        context = super(FinAdminDelete, self).get_context_data(**kwargs)
        form = self.form_class(instance=self.get_object(self))
        texta = 'Account'
        textb = texta.lower()
        context = {
            'texta': texta,
            'textb': textb,
            'textc': self.get_object(self),
            'form': form,
            'edit_mode': self.edit_mode,
            'delete_mode': self.delete_mode,
            'back': 'finadmin',
        }
        return context


def _get_form(request, formcls, prefix):
    data = request.POST if prefix in next(iter(request.POST.keys())) else None
    return formcls(data, prefix=prefix)


class FlowAdd(TemplateView):
    template_name = 'finance/add.html'

    def get(self, request, *args, **kwargs):
        context = {
            'back': 'view',
            'aform': CashInflowForm(prefix='aform_pre'),
            'bform': CashOutflowForm(prefix='bform_pre')
        }
        # return render(request, template_name, context)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        aform = _get_form(request, CashInflowForm, 'aform_pre')
        bform = _get_form(request, CashOutflowForm, 'bform_pre')
        if aform.is_bound and aform.is_valid():
            form = aform.save(commit=False)
            messages.success(self.request, "This transaction has been recorded.")
            form.save()
        elif bform.is_bound and bform.is_valid():
            form = bform.save(commit=False)
            messages.success(self.request, "This transaction has been recorded.")
            form.save()
        context = {
            'back': 'view',
            'aform': aform,
            'bform': bform,
        }
        # return render(request, template_name, context)
        return self.render_to_response(context)


# def inflowCreate(request):
#     if request.method == "POST":
#         form = CashInflowForm(request.POST)
#         if form.is_valid():
#             inflow = form.save(commit=False)
#             inflow.save()
#     else:
#         form = CashInflowForm()
#     return render(request, 'finance/inflow-form.html', {'form': form})


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
            'form': form,
            'pageTitle': pageTitle,
            'back': 'view',
        }
        return context


# def inflowEdit(request, pk):
#     inflow = get_object_or_404(CashInflow, pk=pk)
#     if request.method == "POST":
#         form = CashInflowForm(request.POST, instance=inflow)
#         if form.is_valid():
#             inflow = form.save(commit=False)
#             inflow.save()
#             # return redirect('inflowEdit', pk=inflow.pk)
#             return redirect('index')
#     else:
#         form = CashInflowForm(instance=inflow)
#     return render(request, 'finance/inflow-form.html', {'form': form})


class InflowEdit(UpdateView):
    model = CashInflow
    form_class = CashInflowForm
    template_name = 'finance/add.html'

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
        return redirect('view')
        # return render(self.request, 'finance/generic-form.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(InflowEdit, self).get_context_data(**kwargs)
        form = self.form_class(instance=self.get_object(self))
        pageTitle = 'Edit Cash Inflow'
        context = {
            'aform': form,
            'pageTitle': pageTitle,
            'back': 'view',
        }
        return context


def inflowDelete(request, pk, slug):
    if request.method == 'POST':
        inflow = get_object_or_404(CashInflow, pk=pk)
        inflow.delete()
        messages.success(request, "The transaction has been deleted successfully.")
    # outflows = outflow.objects.filter(user=request.user)
    return redirect('view')


# class InflowDelete(DeleteView):
#     model = CashInflow
#     template_name = 'finance/delete-template.html'
#     success_url = reverse_lazy('view')

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, "The transaction has been deleted successfully.")
#         return super(InflowDelete, self).delete(self, request, *args, **kwargs)

#     def get_object(self, queryset=None):
#         inflow = self.model.objects.get(pk=self.kwargs['pk'])
#         return inflow

#     def get_context_data(self, **kwargs):
#         context = super(InflowDelete, self).get_context_data(**kwargs)
#         texta = 'Inflow'
#         textb = texta.lower()
#         context = {
#             'texta': texta,
#             'textb': textb,
#             'textc': self.get_object(self),
#             'back': 'view',
#         }
#         return context


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
            'aform': form,
            'pageTitle': pageTitle,
            'back': 'view',
        }
        return context


class OutflowEdit(UpdateView):
    model = CashOutflow
    form_class = CashOutflowForm
    template_name = 'finance/add.html'

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
        return redirect('view')
        # return render(self.request, 'finance/generic-form.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(OutflowEdit, self).get_context_data(**kwargs)
        form = self.form_class(instance=self.get_object(self))
        pageTitle = 'Edit Cash Outflow'
        context = {
            'bform': form,
            'pageTitle': pageTitle,
            'back': 'view',
        }
        return context


def outflowDelete(request, pk, slug):
    if request.method == 'POST':
        outflow = get_object_or_404(CashInflow, pk=pk)
        outflow.delete()
        messages.success(request, "The transaction has been deleted successfully.")
    # outflows = outflow.objects.filter(user=request.user)
    return redirect('view')
