# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-28 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rssgenerator', '0006_rss_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='link',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
