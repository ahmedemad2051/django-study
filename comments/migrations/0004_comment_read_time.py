# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-07-01 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20160629_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='read_time',
            field=models.FloatField(null=True),
        ),
    ]