# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-03-03 17:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0010_auto_20200303_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certmodel',
            name='account',
        ),
    ]
