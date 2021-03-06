# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 03:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Content_Management', '0014_auto_20170510_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=100)),
                ('position_desc', models.CharField(max_length=300, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='activities',
            name='requirement',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='requirement',
        ),
        migrations.RemoveField(
            model_name='skillset',
            name='requirement',
        ),
        migrations.DeleteModel(
            name='Requirements',
        ),
        migrations.AddField(
            model_name='activities',
            name='position',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Content_Management.Positions'),
        ),
        migrations.AddField(
            model_name='questions',
            name='position',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Content_Management.Positions'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skillset',
            name='position',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Content_Management.Positions'),
        ),
    ]
