# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0006_auto_20170309_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='piece',
            name='publisheddate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='piece',
            name='url',
            field=models.TextField(blank=True, default=''),
        ),
    ]