# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Content_Management', '0015_auto_20170513_0348'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='position',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Content_Management.Positions'),
        ),
    ]