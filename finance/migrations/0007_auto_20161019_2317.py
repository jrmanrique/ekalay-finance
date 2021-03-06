# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 15:17
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20161019_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashinflow',
            name='chart',
        ),
        migrations.RemoveField(
            model_name='cashoutflow',
            name='chart',
        ),
        migrations.AlterField(
            model_name='cashinflow',
            name='account_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.ChartOfAccounts'),
        ),
        migrations.AlterField(
            model_name='cashoutflow',
            name='account_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.ChartOfAccounts'),
        ),
    ]
