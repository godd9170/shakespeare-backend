# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0030_auto_20170405_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='linkedinhandle',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
