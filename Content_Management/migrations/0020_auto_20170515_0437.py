# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-15 04:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Content_Management', '0019_auto_20170515_0419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skillset',
            old_name='master_field',
            new_name='master_skill',
        ),
    ]
