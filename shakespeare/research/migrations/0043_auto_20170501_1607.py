# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-01 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0042_merge_20170417_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='clearbit',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
