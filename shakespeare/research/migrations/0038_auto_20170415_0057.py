# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-15 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0037_auto_20170415_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='group',
            field=models.CharField(choices=[('article', 'article'), ('expansion', 'expansion'), ('aquisition', 'aquisition'), ('recognition', 'recognition'), ('cost_cutting', 'cost_cutting'), ('investment', 'investment'), ('corporate_challenges', 'corporate_challenges'), ('testimonial', 'testimonial'), ('job_position', 'job_position'), ('new_offering', 'new_offering'), ('leadership', 'leadership'), ('partnership', 'partnership')], default='article', max_length=100),
        ),
    ]
