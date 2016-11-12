from calendar import month_name, monthrange  # Currently unused.

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CashInflowForm, CashOutflowForm, ChartOfAccountsForm, StatementForm
from .functions import *
from .models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts


@user_passes_test(is_council)
def index(request):
    context = {
        'all_inflows': CashInflow.objects.all(),
        'all_outflows': CashOutflow.objects.all(),
        'all_accounts': ChartOfAccounts.objects.all(),
        'total_inflow': sum_flow(CashInflow),
        'total_outflow': sum_flow(CashOutflow),
        'balance': get_balance(),
        'test_mode': test_mode,
        'title': get_field(num),
        'total_title': sum_refnum_net(num),
        'type': get_type(num),
        'total_type': sum_type_net(get_type(num)),
        'test': from_date,
    }
    return render(request, 'finance/index.html', context)


@user_passes_test(is_council)
def statement(request):
    form, from_date, to_date = statement_filter(request)
    context = {
        'total_inflow': sum_flow(CashInflow),
        'total_outflow': sum_flow(CashOutflow),
        'list_accounts': list_accounts(),
        'list_types': list_types(),
        'balance': get_balance(),
        'in_bank': Decimal(in_bank).quantize(Decimal('.01')),
        'form': form,
        'from': parse_date(from_date),
        'to': parse_date(to_date),
    }
    return render(request, 'finance/statement.html', context)


@method_decorator(user_passes_test(is_finance), name='dispatch')
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


@method_decorator(user_passes_test(is_finance), name='dispatch')
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


@method_decorator(user_passes_test(is_finance), name='dispatch')
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


@method_decorator(user_passes_test(is_finance), name='dispatch')
class FlowAdd(TemplateView):
    template_name = 'finance/add.html'

    def get(self, request, *args, **kwargs):
        context = {
            'back': 'view',
            'aform': CashInflowForm(prefix='aform_pre'),
            'bform': CashOutflowForm(prefix='bform_pre'),
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


# class InflowCreate(CreateView):
#     form_class = CashInflowForm
#     template_name = 'finance/generic-form.html'

#     def form_valid(self, form):
#         form.save()
#         messages.success(self.request, "This transaction has been recorded.")
#         return render(self.request, 'finance/generic-form.html', self.get_context_data())

#     def get_context_data(self, **kwargs):
#         context = super(InflowCreate, self).get_context_data(**kwargs)
#         form = self.form_class()
#         pageTitle = 'Add Cash Inflow'
#         context = {
#             'form': form,
#             'pageTitle': pageTitle,
#             'back': 'view',
#         }
#         return context


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


@method_decorator(user_passes_test(is_finance), name='dispatch')
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
        model = 'Inflow'
        context = {
            'aform': form,
            'bform': form,
            'back': 'view',
            'mode': model,
        }
        return context


@user_passes_test(is_finance)
def inflow_delete(request, pk, slug):
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


@method_decorator(user_passes_test(is_finance), name='dispatch')
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
        model = 'Outflow'
        context = {
            'aform': form,
            'bform': form,
            'back': 'view',
            'mode': model,
        }
        return context


@user_passes_test(is_finance)
def outflow_delete(request, pk, slug):
    if request.method == 'POST':
        outflow = get_object_or_404(CashInflow, pk=pk)
        outflow.delete()
        messages.success(request, "The transaction has been deleted successfully.")
    # outflows = outflow.objects.filter(user=request.user)
    return redirect('view')


@user_passes_test(is_super)
def reload_db(request):
    reload_database()
    return redirect('view')
