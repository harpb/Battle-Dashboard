# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.db.utils import OperationalError


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Player.current_win_streak'
        db.alter_column(u'battle_player', 'current_win_streak', self.gf('django.db.models.fields.IntegerField')())

        try:
            # Removing index on 'Player', fields ['nickname']
            db.delete_index(u'battle_player', ['nickname'])
        except OperationalError:
            pass

        # Adding unique constraint on 'Player', fields ['nickname']
        db.create_unique(u'battle_player', ['nickname'])


    def backwards(self, orm):
        # Removing unique constraint on 'Player', fields ['nickname']
        db.delete_unique(u'battle_player', ['nickname'])

        # Adding index on 'Player', fields ['nickname']
        db.create_index(u'battle_player', ['nickname'])

        # Changing field 'Player.current_win_streak'
        db.alter_column(u'battle_player', 'current_win_streak', self.gf('django.db.models.fields.PositiveIntegerField')())

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
            'current_win_streak': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'losses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'nickname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'wins': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['battle']
