# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rssgenerator', '0002_links_storelocaly'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='storeLocaly',
            field=models.BooleanField(default=True),
        ),
    ]
