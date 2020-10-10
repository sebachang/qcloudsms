# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-01-08 15:02
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('deliver_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliverOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vlan', models.CharField(blank=True, max_length=255, null=True)),
                ('system', models.CharField(max_length=255)),
                ('amount', models.IntegerField(default=1)),
                ('desc', models.CharField(max_length=255)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('center_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING,
                                                to='deliver_manage.Center')),
                ('host_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING,
                                              to='deliver_manage.HostProfile')),
                ('platform_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING,
                                                  to='deliver_manage.Platform')),
            ],
            options={
                'db_table': 'order_center_deliver_deliver_order',
            },
        ),
    ]
