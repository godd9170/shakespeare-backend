# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0028_auto_20170403_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='group',
            field=models.CharField(choices=[('cost_cutting', 'cost_cutting'), ('partnership', 'partnership'), ('article', 'article'), ('job_position', 'job_position'), ('investment', 'investment'), ('new_offering', 'new_offering'), ('expansion', 'expansion'), ('corporate_challenges', 'corporate_challenges'), ('recognition', 'recognition'), ('testimonial', 'testimonial'), ('aquisition', 'aquisition'), ('leadership', 'leadership')], default='article', max_length=100),
        ),
    ]
