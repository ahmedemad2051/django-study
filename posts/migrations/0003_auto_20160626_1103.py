# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-06-26 11:03
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to=posts.models.upload_location),
        ),
    ]