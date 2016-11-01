# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashInflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('inflow_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CashOutflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('outflow_type', models.CharField(max_length=100)),
            ],
        ),
    ]
