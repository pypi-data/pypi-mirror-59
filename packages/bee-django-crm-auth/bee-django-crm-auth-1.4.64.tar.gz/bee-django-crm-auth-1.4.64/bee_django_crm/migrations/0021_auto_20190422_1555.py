# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-04-22 07:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_crm', '0020_regcode_reg_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='regcode',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterModelTable(
            name='regcode',
            table='bee_django_crm_code',
        ),
    ]
