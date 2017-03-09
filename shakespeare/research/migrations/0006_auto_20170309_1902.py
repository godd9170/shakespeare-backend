# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0005_auto_20170308_2206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nugget',
            old_name='actor',
            new_name='entity',
        ),
        migrations.AddField(
            model_name='nugget',
            name='category',
            field=models.CharField(choices=[('quote', 'Quote'), ('tweet', 'Tweet'), ('joblisting', 'Job Listing')], default='quote', max_length=100),
        ),
    ]