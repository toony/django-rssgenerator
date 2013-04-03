# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rss'
        db.create_table(u'rssgenerator_rss', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=1024)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'rssgenerator', ['Rss'])

        # Adding model 'Items'
        db.create_table(u'rssgenerator_items', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rss', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rssgenerator.Rss'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=1024)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'rssgenerator', ['Items'])

        # Adding model 'Links'
        db.create_table(u'rssgenerator_links', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rssgenerator.Items'])),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=1024)),
        ))
        db.send_create_signal(u'rssgenerator', ['Links'])


    def backwards(self, orm):
        # Deleting model 'Rss'
        db.delete_table(u'rssgenerator_rss')

        # Deleting model 'Items'
        db.delete_table(u'rssgenerator_items')

        # Deleting model 'Links'
        db.delete_table(u'rssgenerator_links')


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
            'link': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['rssgenerator']