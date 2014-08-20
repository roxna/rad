# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Roaming.duration'
        db.add_column(u'bills_roaming', 'duration',
                      self.gf('django.db.models.fields.CharField')(default='00:00', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Roaming.volume'
        db.add_column(u'bills_roaming', 'volume',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=6, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.duration'
        db.add_column(u'bills_data', 'duration',
                      self.gf('django.db.models.fields.CharField')(default='00:00', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.volume'
        db.add_column(u'bills_data', 'volume',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=6, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Booster.duration'
        db.add_column(u'bills_booster', 'duration',
                      self.gf('django.db.models.fields.CharField')(default='00:00', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Booster.volume'
        db.add_column(u'bills_booster', 'volume',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=6, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Call.duration'
        db.add_column(u'bills_call', 'duration',
                      self.gf('django.db.models.fields.CharField')(default='00:00', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Call.volume'
        db.add_column(u'bills_call', 'volume',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=6, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Roaming.duration'
        db.delete_column(u'bills_roaming', 'duration')

        # Deleting field 'Roaming.volume'
        db.delete_column(u'bills_roaming', 'volume')

        # Deleting field 'Data.duration'
        db.delete_column(u'bills_data', 'duration')

        # Deleting field 'Data.volume'
        db.delete_column(u'bills_data', 'volume')

        # Deleting field 'Booster.duration'
        db.delete_column(u'bills_booster', 'duration')

        # Deleting field 'Booster.volume'
        db.delete_column(u'bills_booster', 'volume')

        # Deleting field 'Call.duration'
        db.delete_column(u'bills_call', 'duration')

        # Deleting field 'Call.volume'
        db.delete_column(u'bills_call', 'volume')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'bills.bill': {
            'Meta': {'object_name': 'Bill'},
            'bill_date': ('django.db.models.fields.DateField', [], {'default': '1998'}),
            'booster_charge': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'call_charge': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'data_charge': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'default': '1998'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': '1998'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'late_fee': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'monthly_charge': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'onetime_charge': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill'", 'to': u"orm['bills.Plan']"}),
            'roaming_charge': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': '1998'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill'", 'to': u"orm['bills.Subscriber']"}),
            'tax': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'total_bill': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'})
        },
        u'bills.booster': {
            'Meta': {'object_name': 'Booster'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'booster'", 'to': u"orm['bills.Bill']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'default': '1998'}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'00:00'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_number': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(12, 12, 12)'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '70'}),
            'volume': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '6', 'null': 'True', 'blank': 'True'})
        },
        u'bills.call': {
            'Meta': {'object_name': 'Call'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'call'", 'to': u"orm['bills.Bill']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'default': '1998'}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'00:00'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_number': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(12, 12, 12)'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '70'}),
            'volume': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '6', 'null': 'True', 'blank': 'True'})
        },
        u'bills.data': {
            'Meta': {'object_name': 'Data'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data'", 'to': u"orm['bills.Bill']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'default': '1998'}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'00:00'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_number': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(12, 12, 12)'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '70'}),
            'volume': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '6', 'null': 'True', 'blank': 'True'})
        },
        u'bills.plan': {
            'Meta': {'object_name': 'Plan'},
            'currency': ('django.db.models.fields.CharField', [], {'default': "'INR'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_rental': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '20'})
        },
        u'bills.roaming': {
            'Meta': {'object_name': 'Roaming'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roaming'", 'to': u"orm['bills.Bill']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'default': '1998'}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'00:00'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_number': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(12, 12, 12)'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '70'}),
            'volume': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '6', 'null': 'True', 'blank': 'True'})
        },
        u'bills.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'credit_limit': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'phone_number': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'relationship_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'security_deposit': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        u'bills.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'../static/img/profile_pics/default_profile_pic.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bills']