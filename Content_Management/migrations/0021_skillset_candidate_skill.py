# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Content_Management', '0020_auto_20170515_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='skillset',
            name='candidate_skill',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
