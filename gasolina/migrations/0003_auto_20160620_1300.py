# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 13:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gasolina', '0002_auto_20160619_2009'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Usuario',
        ),
    ]