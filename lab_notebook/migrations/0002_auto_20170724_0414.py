# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-24 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab_notebook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labnote',
            name='note_date',
            field=models.DateField(verbose_name='date created'),
        ),
    ]
