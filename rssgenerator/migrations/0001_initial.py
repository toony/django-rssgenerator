# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('link', models.URLField(max_length=1024)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('summary', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.URLField(max_length=1024)),
                ('item', models.ForeignKey(to='rssgenerator.Items')),
            ],
        ),
        migrations.CreateModel(
            name='Rss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='rss',
            field=models.ForeignKey(to='rssgenerator.Rss'),
        ),
    ]
