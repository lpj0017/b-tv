# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VideoURL.is_saved'
        db.add_column('myapp_videourl', 'is_saved',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'VideoURL.is_saved'
        db.delete_column('myapp_videourl', 'is_saved')


    models = {
        'myapp.part': {
            'Meta': {'object_name': 'Part'},
            'cid': ('django.db.models.fields.IntegerField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp4': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Video']"})
        },
        'myapp.topic': {
            'Meta': {'object_name': 'Topic'},
            'clicked': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'myapp.video': {
            'Meta': {'object_name': 'Video'},
            'aid': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'myapp.videourl': {
            'Meta': {'object_name': 'VideoURL'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_saved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['myapp']