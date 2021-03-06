# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 18:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0009_auto_20170313_2232'),
        ('research', '0023_auto_20170322_1710'),
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='nugget',
        ),
        migrations.AddField(
            model_name='email',
            name='body',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='email',
            name='selectedcalltoaction',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='selectedcalltoaction', to='personas.CallToAction'),
        ),
        migrations.AddField(
            model_name='email',
            name='selectednugget',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='selectednugget', to='research.Nugget'),
        ),
        migrations.AddField(
            model_name='email',
            name='selectedvalueproposition',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='selectedvalueproposition', to='personas.ValueProposition'),
        ),
        migrations.AlterField(
            model_name='email',
            name='gmailid',
            field=models.TextField(),
        ),
    ]
