# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2020-01-08 07:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_crm', '0050_auto_20200108_1451'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bargainreward',
            options={'ordering': ['pk'], 'permissions': (('view_bargain_reward_detail', 'view_bargain_reward_detail'),)},
        ),
    ]
