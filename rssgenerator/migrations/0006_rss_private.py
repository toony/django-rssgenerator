# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-28 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rssgenerator', '0005_links_fromuploadedfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='rss',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
