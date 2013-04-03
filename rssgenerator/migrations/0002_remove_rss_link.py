# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Rss.link'
        db.delete_column(u'rssgenerator_rss', 'link')


    def backwards(self, orm):
        # Adding field 'Rss.link'
        db.add_column(u'rssgenerator_rss', 'link',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=1024),
                      keep_default=False)


    models = {
        u'rssgenerator.items': {
            'Meta': {'object_name': 'Items'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'rss': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rssgenerator.Rss']"}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'rssgenerator.links': {
            'Meta': {'object_name': 'Links'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rssgenerator.Items']"}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '1024'})
        },
        u'rssgenerator.rss': {
            'Meta': {'object_name': 'Rss'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['rssgenerator']