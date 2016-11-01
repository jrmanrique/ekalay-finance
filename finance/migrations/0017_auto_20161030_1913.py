# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 11:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0016_auto_20161030_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(max_length=100, verbose_name='Account Type')),
            ],
            options={
                'verbose_name': 'Account Types',
            },
        ),
        migrations.AlterField(
            model_name='chartofaccounts',
            name='account_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.AccountTypes', verbose_name='Account Type'),
        ),
    ]
