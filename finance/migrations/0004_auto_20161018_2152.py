# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20161018_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashinflow',
            name='account_title',
            field=models.CharField(default=0, max_length=100, verbose_name='Account Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cashinflow',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=29),
        ),
        migrations.AddField(
            model_name='cashinflow',
            name='document',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cashinflow',
            name='notes',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='cashinflow',
            name='payor',
            field=models.CharField(default=0, max_length=100, verbose_name="Payor's Name"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cashinflow',
            name='ref_num',
            field=models.IntegerField(default=0, verbose_name='Reference Number'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cashinflow',
            name='remarks',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='cashoutflow',
            name='payor',
            field=models.CharField(default=9, max_length=100, verbose_name="Payee's Name"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cashinflow',
            name='inflow_type',
            field=models.CharField(max_length=100, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='cashoutflow',
            name='account_title',
            field=models.CharField(max_length=100, verbose_name='Account Title'),
        ),
        migrations.AlterField(
            model_name='cashoutflow',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=29),
        ),
        migrations.AlterField(
            model_name='cashoutflow',
            name='document',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='cashoutflow',
            name='outflow_type',
            field=models.CharField(max_length=100, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='cashoutflow',
            name='purpose',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='cashoutflow',
            name='ref_num',
            field=models.IntegerField(verbose_name='Reference Number'),
        ),
    ]
