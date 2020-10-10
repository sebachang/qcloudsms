# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-03-03 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biz_id', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
