# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'NewsPost.page_ptr'
        db.delete_column(u'news_newspost', u'page_ptr_id')

        # Adding field 'NewsPost.id'
        db.add_column(u'news_newspost', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Adding field 'NewsPost.keywords_string'
        db.add_column(u'news_newspost', 'keywords_string',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True),
                      keep_default=False)

        # Adding field 'NewsPost.site'
        db.add_column(u'news_newspost', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['sites.Site']),
                      keep_default=False)

        # Adding field 'NewsPost.title'
        db.add_column(u'news_newspost', 'title',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=500),
                      keep_default=False)

        # Adding field 'NewsPost.slug'
        db.add_column(u'news_newspost', 'slug',
                      self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'NewsPost._meta_title'
        db.add_column(u'news_newspost', '_meta_title',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)

        # Adding field 'NewsPost.description'
        db.add_column(u'news_newspost', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'NewsPost.gen_description'
        db.add_column(u'news_newspost', 'gen_description',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'NewsPost.status'
        db.add_column(u'news_newspost', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

        # Adding field 'NewsPost.publish_date'
        db.add_column(u'news_newspost', 'publish_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'NewsPost.expiry_date'
        db.add_column(u'news_newspost', 'expiry_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'NewsPost.short_url'
        db.add_column(u'news_newspost', 'short_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'NewsPost.in_sitemap'
        db.add_column(u'news_newspost', 'in_sitemap',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'NewsPost.theme_color'
        db.add_column(u'news_newspost', 'theme_color',
                      self.gf('django.db.models.fields.CharField')(default='grey', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'NewsPost.page_ptr'
        db.add_column(u'news_newspost', u'page_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['pages.Page'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'NewsPost.id'
        db.delete_column(u'news_newspost', u'id')

        # Deleting field 'NewsPost.keywords_string'
        db.delete_column(u'news_newspost', 'keywords_string')

        # Deleting field 'NewsPost.site'
        db.delete_column(u'news_newspost', 'site_id')

        # Deleting field 'NewsPost.title'
        db.delete_column(u'news_newspost', 'title')

        # Deleting field 'NewsPost.slug'
        db.delete_column(u'news_newspost', 'slug')

        # Deleting field 'NewsPost._meta_title'
        db.delete_column(u'news_newspost', '_meta_title')

        # Deleting field 'NewsPost.description'
        db.delete_column(u'news_newspost', 'description')

        # Deleting field 'NewsPost.gen_description'
        db.delete_column(u'news_newspost', 'gen_description')

        # Deleting field 'NewsPost.status'
        db.delete_column(u'news_newspost', 'status')

        # Deleting field 'NewsPost.publish_date'
        db.delete_column(u'news_newspost', 'publish_date')

        # Deleting field 'NewsPost.expiry_date'
        db.delete_column(u'news_newspost', 'expiry_date')

        # Deleting field 'NewsPost.short_url'
        db.delete_column(u'news_newspost', 'short_url')

        # Deleting field 'NewsPost.in_sitemap'
        db.delete_column(u'news_newspost', 'in_sitemap')

        # Deleting field 'NewsPost.theme_color'
        db.delete_column(u'news_newspost', 'theme_color')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'generic.assignedkeyword': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AssignedKeyword'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['generic.Keyword']"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        u'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'news.newspost': {
            'Meta': {'object_name': 'NewsPost'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'theme_color': ('django.db.models.fields.CharField', [], {'default': "'grey'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['news']