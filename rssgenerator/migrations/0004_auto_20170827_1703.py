# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from rssgenerator.LocalStore import LocalStore

def updateLinksHeightWidth(apps, schema_editor):
    Rss = apps.get_model("rssgenerator", "Rss")
    Links = apps.get_model("rssgenerator", "Links")
    db_alias = schema_editor.connection.alias
    
    for rss in Rss.objects.using(db_alias).all():
        localStore = LocalStore(rss.id)
        
        for item in rss.items_set.all():
            for link in item.links_set.all():
                infos = localStore.setHeightWidth(item.id, link)

                Links.objects.filter(id = link.id) \
                             .update(height = infos ['h'],
                                     width = infos['w'])

class Migration(migrations.Migration):

    dependencies = [
        ('rssgenerator', '0003_auto_20170427_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='height',
            field=models.IntegerField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='links',
            name='width',
            field=models.IntegerField(null=True, editable=False),
        ),
        migrations.RunPython(updateLinksHeightWidth),
    ]
