# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0031_individual_linkedinhandle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='linkedinhandle',
            field=models.TextField(blank=True, null=True),
        ),
    ]
