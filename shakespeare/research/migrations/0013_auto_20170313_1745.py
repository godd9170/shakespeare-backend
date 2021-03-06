# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 17:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0012_auto_20170313_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ('created',), 'verbose_name': 'company', 'verbose_name_plural': 'companies'},
        ),
        migrations.AlterModelOptions(
            name='individual',
            options={'ordering': ('created',), 'verbose_name': 'individual', 'verbose_name_plural': 'individuals'},
        ),
        migrations.AlterModelOptions(
            name='nugget',
            options={'ordering': ('created',), 'verbose_name': 'nugget', 'verbose_name_plural': 'nuggets'},
        ),
        migrations.AlterModelOptions(
            name='piece',
            options={'ordering': ('created',), 'verbose_name': 'piece', 'verbose_name_plural': 'pieces'},
        ),
        migrations.AlterModelOptions(
            name='research',
            options={'ordering': ('created',), 'verbose_name': 'research', 'verbose_name_plural': 'research'},
        ),
    ]
