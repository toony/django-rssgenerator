# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rssgenerator', '0004_auto_20170827_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='fromUploadedFile',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='links',
            name='link',
            field=models.URLField(max_length=1024, null=True, blank=True),
        ),
    ]
