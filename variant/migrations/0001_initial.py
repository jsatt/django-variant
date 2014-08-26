# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Experiment'
        db.create_table(u'variant_experiment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('variants', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'variant', ['Experiment'])


    def backwards(self, orm):
        # Deleting model 'Experiment'
        db.delete_table(u'variant_experiment')


    models = {
        u'variant.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'variants': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['variant']