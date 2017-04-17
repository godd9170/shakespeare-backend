# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0022_auto_20170320_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nugget',
            name='category',
            field=models.CharField(choices=[('quote_from_individual', 'Quote From Individual'), ('quote_from_company', 'Quote From Company'), ('quote_about', 'Quote About'), ('testimonial', 'Testimonial'), ('hires', 'Hires'), ('promotes', 'Promotes'), ('leaves', 'Leaves'), ('retires', 'Retires'), ('acquires', 'Aquires'), ('merges_with', 'Merges With'), ('sells_assets_to', 'Sells Assets To'), ('expands_offices_to', 'Expands Offices To'), ('expands_offices_in', 'Expands Office In'), ('expands_facilities', 'Expands Facilities'), ('opens_new_location', 'Opens New Location'), ('increases_headcount_by', 'Increases Headcount By'), ('launches', 'Launches'), ('integrates_with', 'Integrates With'), ('is_developing', 'Is Developing'), ('receives_financing', 'Receives Financing'), ('invests_into', 'Invests Into'), ('goes_public', 'Goes Public'), ('closes_offices', 'Closes Offices'), ('decreases_headcount_by', 'Decreases Headcount By'), ('partners_with', 'Partners With'), ('receives_award', 'Receives Award'), ('recognized_as', 'Recognized As'), ('signs_new_client', 'Signs New Client'), ('files_suit_against', 'Files Suit Against'), ('has_issues_with', 'Has Issues With'), ('none', 'None'), ('administration', 'Administration'), ('chairmen', 'Chairmen'), ('health_care', 'Health Care'), ('hospitality', 'Hospitality'), ('engineering', 'Engineering'), ('education', 'Education'), ('maintenance', 'Maintenance'), ('finance', 'Finance'), ('information_technology', 'Information Technology'), ('management', 'Management'), ('operations', 'Operations'), ('partnerships', 'Partnerships'), ('human_resources', 'Human Resources'), ('publishing', 'Publishing'), ('purchasing', 'Purchasing'), ('sales', 'Sales'), ('marketing', 'Marketing'), ('transportation', 'Transportation'), ('directors', 'Directors'), ('design', 'Design'), ('software_development', 'Software Development'), ('general_technology', 'General Technology'), ('business_analysis', 'Business Analysis'), ('support', 'Support'), ('data_analysis', 'Data Analysis')], default='quote', max_length=100),
        ),
        migrations.AlterField(
            model_name='nuggettemplate',
            name='category',
            field=models.CharField(choices=[('quote_from_individual', 'Quote From Individual'), ('quote_from_company', 'Quote From Company'), ('quote_about', 'Quote About'), ('testimonial', 'Testimonial'), ('hires', 'Hires'), ('promotes', 'Promotes'), ('leaves', 'Leaves'), ('retires', 'Retires'), ('acquires', 'Aquires'), ('merges_with', 'Merges With'), ('sells_assets_to', 'Sells Assets To'), ('expands_offices_to', 'Expands Offices To'), ('expands_offices_in', 'Expands Office In'), ('expands_facilities', 'Expands Facilities'), ('opens_new_location', 'Opens New Location'), ('increases_headcount_by', 'Increases Headcount By'), ('launches', 'Launches'), ('integrates_with', 'Integrates With'), ('is_developing', 'Is Developing'), ('receives_financing', 'Receives Financing'), ('invests_into', 'Invests Into'), ('goes_public', 'Goes Public'), ('closes_offices', 'Closes Offices'), ('decreases_headcount_by', 'Decreases Headcount By'), ('partners_with', 'Partners With'), ('receives_award', 'Receives Award'), ('recognized_as', 'Recognized As'), ('signs_new_client', 'Signs New Client'), ('files_suit_against', 'Files Suit Against'), ('has_issues_with', 'Has Issues With'), ('none', 'None'), ('administration', 'Administration'), ('chairmen', 'Chairmen'), ('health_care', 'Health Care'), ('hospitality', 'Hospitality'), ('engineering', 'Engineering'), ('education', 'Education'), ('maintenance', 'Maintenance'), ('finance', 'Finance'), ('information_technology', 'Information Technology'), ('management', 'Management'), ('operations', 'Operations'), ('partnerships', 'Partnerships'), ('human_resources', 'Human Resources'), ('publishing', 'Publishing'), ('purchasing', 'Purchasing'), ('sales', 'Sales'), ('marketing', 'Marketing'), ('transportation', 'Transportation'), ('directors', 'Directors'), ('design', 'Design'), ('software_development', 'Software Development'), ('general_technology', 'General Technology'), ('business_analysis', 'Business Analysis'), ('support', 'Support'), ('data_analysis', 'Data Analysis')], default='quote', max_length=100),
        ),
    ]