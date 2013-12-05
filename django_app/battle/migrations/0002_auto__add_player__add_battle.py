# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'battle_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=30, blank=True)),
            ('current_win_streak', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('losses', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('wins', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'battle', ['Player'])

        # Adding model 'Battle'
        db.create_table(u'battle_battle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('attacker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attacker', to=orm['battle.Player'])),
            ('defender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='defender', to=orm['battle.Player'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winner', to=orm['battle.Player'])),
        ))
        db.send_create_signal(u'battle', ['Battle'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'battle_player')

        # Deleting model 'Battle'
        db.delete_table(u'battle_battle')


    models = {
        u'battle.battle': {
            'Meta': {'object_name': 'Battle'},
            'attacker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attacker'", 'to': u"orm['battle.Player']"}),
            'defender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'defender'", 'to': u"orm['battle.Player']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner'", 'to': u"orm['battle.Player']"})
        },
        u'battle.player': {
            'Meta': {'object_name': 'Player'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'current_win_streak': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'losses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'nickname': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'blank': 'True'}),
            'wins': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['battle']