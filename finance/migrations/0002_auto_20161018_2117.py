# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 13:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cashinflow',
            options={'verbose_name': 'Cash Inflow'},
        ),
        migrations.AlterModelOptions(
            name='cashoutflow',
            options={'verbose_name': 'Cash Outflow'},
        ),
    ]
