# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-09-23 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_crm', '0028_auto_20190911_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preuser',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, b'\xe7\x94\xb7'), (2, b'\xe5\xa5\xb3')], default=0, null=True, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab'),
        ),
    ]
