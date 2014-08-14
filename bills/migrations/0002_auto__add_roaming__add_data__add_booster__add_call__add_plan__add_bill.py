# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Roaming'
        db.create_table(u'bills_roaming', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('recipient_number', self.gf('django.db.models.fields.IntegerField')()),
            ('vol_or_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roaming', to=orm['bills.Bill'])),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=70)),
        ))
        db.send_create_signal(u'bills', ['Roaming'])

        # Adding model 'Data'
        db.create_table(u'bills_data', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('recipient_number', self.gf('django.db.models.fields.IntegerField')()),
            ('vol_or_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='data', to=orm['bills.Bill'])),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=70)),
        ))
        db.send_create_signal(u'bills', ['Data'])

        # Adding model 'Booster'
        db.create_table(u'bills_booster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('recipient_number', self.gf('django.db.models.fields.IntegerField')()),
            ('vol_or_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='booster', to=orm['bills.Bill'])),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=70)),
        ))
        db.send_create_signal(u'bills', ['Booster'])

        # Adding model 'Call'
        db.create_table(u'bills_call', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('recipient_number', self.gf('django.db.models.fields.IntegerField')()),
            ('vol_or_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='call', to=orm['bills.Bill'])),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=70)),
        ))
        db.send_create_signal(u'bills', ['Call'])

        # Adding model 'Plan'
        db.create_table(u'bills_plan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('min_rental', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'bills', ['Plan'])

        # Adding model 'Bill'
        db.create_table(u'bills_bill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('bill_date', self.gf('django.db.models.fields.DateField')()),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('total_bill', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('onetime_charge', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('monthly_charge', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('call_charge', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('booster_charge', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('data_charge', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('roaming_charge', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('late_fee', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=7, decimal_places=2, blank=True)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bill', to=orm['bills.Subscriber'])),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bill', to=orm['bills.Plan'])),
        ))
        db.send_create_signal(u'bills', ['Bill'])

        # Adding model 'User'
        db.create_table(u'bills_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default='../static/img/profile_pics/default_profile_pic.png', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'bills', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'bills_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'bills.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name(u'bills_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'bills.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding model 'Subscriber'
        db.create_table(u'bills_subscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('zip', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('relationship_num', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('credit_limit', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=2)),
        ))
        db.send_create_signal(u'bills', ['Subscriber'])


    def backwards(self, orm):
        # Deleting model 'Roaming'
        db.delete_table(u'bills_roaming')

        # Deleting model 'Data'
        db.delete_table(u'bills_data')

        # Deleting model 'Booster'
        db.delete_table(u'bills_booster')

        # Deleting model 'Call'
        db.delete_table(u'bills_call')

        # Deleting model 'Plan'
        db.delete_table(u'bills_plan')

        # Deleting model 'Bill'
        db.delete_table(u'bills_bill')

        # Deleting model 'User'
        db.delete_table(u'bills_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'bills_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name(u'bills_user_user_permissions'))

        # Deleting model 'Subscriber'
        db.delete_table(u'bills_subscriber')


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
            'bill_date': ('django.db.models.fields.DateField', [], {}),
            'booster_charge': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'call_charge': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'data_charge': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'late_fee': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'monthly_charge': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'onetime_charge': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill'", 'to': u"orm['bills.Plan']"}),
            'roaming_charge': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bill'", 'to': u"orm['bills.Subscriber']"}),
            'tax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'total_bill': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        },
        u'bills.booster': {
            'Meta': {'object_name': 'Booster'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'booster'", 'to': u"orm['bills.Bill']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_number': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '70'}),
            'vol_or_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'bills.call': {
            'Meta': {'object_name': 'Call'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'call'", 'to': u"orm['bills.Bill']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_number': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '70'}),
            'vol_or_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'bills.data': {
            'Meta': {'object_name': 'Data'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data'", 'to': u"orm['bills.Bill']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_number': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '70'}),
            'vol_or_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'bills.plan': {
            'Meta': {'object_name': 'Plan'},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_rental': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '20'})
        },
        u'bills.roaming': {
            'Meta': {'object_name': 'Roaming'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roaming'", 'to': u"orm['bills.Bill']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_number': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '70'}),
            'vol_or_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'bills.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'credit_limit': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'relationship_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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