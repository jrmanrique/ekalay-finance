from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


class AccountTypes(models.Model):
    account_type = models.CharField(max_length=100, verbose_name='Account Type')

    class Meta:
        verbose_name = 'Account Type'

    def __str__(self):
        return str(self.account_type)


class ChartOfAccounts(models.Model):
    ref_num = models.PositiveIntegerField(verbose_name='Reference Number', unique=True)
    account_title = models.CharField(max_length=100, verbose_name='Account Title')
    account_type = models.ForeignKey(AccountTypes, verbose_name='Account Type')

    class Meta:
        verbose_name = 'Chart of Account'
        ordering = ('ref_num',)

    def __str__(self):
        return str(self.account_title)

    def get_absolute_url(self):
        kwargs = {
            'pk' : self.pk,
            'ref_num' : self.ref_num,
        }
        return reverse('account-edit', kwargs=kwargs)


class CashInflow(models.Model):
    slug = models.SlugField(default='', editable=False)
    date = models.DateField(default=datetime.now, blank=True)
    flow_type = models.CharField(max_length=100, verbose_name='Type', blank=True)
    ref_num = models.ForeignKey(ChartOfAccounts, to_field='ref_num', verbose_name='Reference Number')
    account_title = models.CharField(max_length=100, verbose_name='Account Title', blank=True)
    # ref_num = models.PositiveIntegerField(verbose_name='Reference Number', blank=True)
    # account_title = models.ForeignKey(ChartOfAccounts, verbose_name='Account Title')
    payor = models.CharField(max_length=100, verbose_name='Payor\'s Name')
    amount = models.DecimalField(default=0, max_digits=29, decimal_places=2)
    document = models.CharField(max_length=250, blank=True)
    notes = models.CharField(max_length=500, blank=True)
    # remarks = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Cash Inflow'
        ordering = ('-date',)

    def __str__(self):
        return str(self.date) + ' ' + str(self.payor) + ' (PHP ' + str(self.amount) +')'

    def save(self, *args, **kwargs):
        # self.ref_num = self.account_title.ref_num
        self.account_title = self.ref_num.account_title
        # self.flow_type = self.account_title.account_type.account_type
        self.flow_type = self.ref_num.account_type.account_type
        if self.document:
            self.slug = slugify(self.ref_num) + '-' + slugify(self.document)
        else:
            self.slug = slugify(self.ref_num) + '-' + slugify(self.payor)
        super(CashInflow, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'pk' : self.pk,
            'slug' : self.slug,
        }
        return reverse('inflow-edit', kwargs=kwargs)


class CashOutflow(models.Model):
    slug = models.SlugField(default='', editable=False)
    date = models.DateField(default=datetime.now, blank=True)
    flow_type = models.CharField(max_length=100, verbose_name='Type', blank=True)
    ref_num = models.PositiveIntegerField(verbose_name='Reference Number', blank=True)
    account_title = models.ForeignKey(ChartOfAccounts, verbose_name='Account Title')
    payee = models.CharField(max_length=100, verbose_name='Payee\'s Name')
    purpose = models.CharField(max_length=500)
    amount = models.DecimalField(default=0, max_digits=29, decimal_places=2)
    document = models.CharField(max_length=250)
    notes = models.CharField(max_length=500, blank=True)
    # remarks = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Cash Outflow'
        ordering = ('-date',)

    def __str__(self):
        return str(self.date) + ' ' + str(self.purpose) + ' (PHP ' + str(self.amount) +')'

    def save(self, *args, **kwargs):
        self.ref_num = self.account_title.ref_num
        self.flow_type = self.account_title.account_type.account_type
        if self.document:
            self.slug = slugify(self.ref_num) + '-' + slugify(self.document)
        else:
            self.slug = slugify(self.ref_num) + '-' + slugify(self.payee)
        super(CashOutflow, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'pk' : self.pk,
            'slug' : self.slug,
        }
        return reverse('outflow-edit', kwargs=kwargs)
