# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0027_auto_20170331_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nugget',
            name='body',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='piece',
            name='body',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]