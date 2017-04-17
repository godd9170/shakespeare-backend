# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-15 00:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0036_auto_20170414_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='group',
            field=models.CharField(choices=[('job_position', 'job_position'), ('cost_cutting', 'cost_cutting'), ('article', 'article'), ('partnership', 'partnership'), ('testimonial', 'testimonial'), ('expansion', 'expansion'), ('recognition', 'recognition'), ('aquisition', 'aquisition'), ('new_offering', 'new_offering'), ('investment', 'investment'), ('leadership', 'leadership'), ('corporate_challenges', 'corporate_challenges')], default='article', max_length=100),
        ),
    ]