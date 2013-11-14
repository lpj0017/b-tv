# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Video'
        db.create_table('myapp_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aid', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('pic_url', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('myapp', ['Video'])

        # Adding model 'Part'
        db.create_table('myapp_part', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cid', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('mp4', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.Video'])),
        ))
        db.send_create_signal('myapp', ['Part'])

        # Adding model 'Topic'
        db.create_table('myapp_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('clicked', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('myapp', ['Topic'])

        # Adding model 'VideoURL'
        db.create_table('myapp_videourl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=2048)),
        ))
        db.send_create_signal('myapp', ['VideoURL'])


    def backwards(self, orm):
        # Deleting model 'Video'
        db.delete_table('myapp_video')

        # Deleting model 'Part'
        db.delete_table('myapp_part')

        # Deleting model 'Topic'
        db.delete_table('myapp_topic')

        # Deleting model 'VideoURL'
        db.delete_table('myapp_videourl')


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
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['myapp']