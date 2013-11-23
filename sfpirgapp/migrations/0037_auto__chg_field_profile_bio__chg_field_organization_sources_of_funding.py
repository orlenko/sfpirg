# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Profile.bio'
        db.alter_column(u'sfpirgapp_profile', 'bio', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'Organization.sources_of_funding'
        db.alter_column(u'sfpirgapp_organization', 'sources_of_funding', self.gf('mezzanine.core.fields.RichTextField')())

        # Changing field 'Organization.mandate'
        db.alter_column(u'sfpirgapp_organization', 'mandate', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'Organization.communities'
        db.alter_column(u'sfpirgapp_organization', 'communities', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'ActionGroup.twoliner'
        db.alter_column(u'sfpirgapp_actiongroup', 'twoliner', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'ActionGroup.timeline'
        db.alter_column(u'sfpirgapp_actiongroup', 'timeline', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'ActionGroup.oneliner'
        db.alter_column(u'sfpirgapp_actiongroup', 'oneliner', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'ActionGroup.potential_members'
        db.alter_column(u'sfpirgapp_actiongroup', 'potential_members', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'ActionGroup.goals'
        db.alter_column(u'sfpirgapp_actiongroup', 'goals', self.gf('mezzanine.core.fields.RichTextField')(null=True))
        # Deleting field 'Project.size'
        db.delete_column(u'sfpirgapp_project', 'size')

        # Deleting field 'Project.description_short'
        db.delete_column(u'sfpirgapp_project', 'description_short')


        # Changing field 'Project.researcher_qualities'
        db.alter_column(u'sfpirgapp_project', 'researcher_qualities', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'Project.description_long'
        db.alter_column(u'sfpirgapp_project', 'description_long', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'Project.results_plan'
        db.alter_column(u'sfpirgapp_project', 'results_plan', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'Project.time_per_week'
        db.alter_column(u'sfpirgapp_project', 'time_per_week', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'Project.support_method'
        db.alter_column(u'sfpirgapp_project', 'support_method', self.gf('mezzanine.core.fields.RichTextField')(null=True))

        # Changing field 'Project.larger_goal'
        db.alter_column(u'sfpirgapp_project', 'larger_goal', self.gf('mezzanine.core.fields.RichTextField')(null=True))
        # Adding field 'Testimonial.author_email'
        db.add_column(u'sfpirgapp_testimonial', 'author_email',
                      self.gf('django.db.models.fields.EmailField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Profile.bio'
        db.alter_column(u'sfpirgapp_profile', 'bio', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Organization.sources_of_funding'
        db.alter_column(u'sfpirgapp_organization', 'sources_of_funding', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Organization.mandate'
        db.alter_column(u'sfpirgapp_organization', 'mandate', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Organization.communities'
        db.alter_column(u'sfpirgapp_organization', 'communities', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'ActionGroup.twoliner'
        db.alter_column(u'sfpirgapp_actiongroup', 'twoliner', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'ActionGroup.timeline'
        db.alter_column(u'sfpirgapp_actiongroup', 'timeline', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'ActionGroup.oneliner'
        db.alter_column(u'sfpirgapp_actiongroup', 'oneliner', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'ActionGroup.potential_members'
        db.alter_column(u'sfpirgapp_actiongroup', 'potential_members', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'ActionGroup.goals'
        db.alter_column(u'sfpirgapp_actiongroup', 'goals', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding field 'Project.size'
        db.add_column(u'sfpirgapp_project', 'size',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.description_short'
        db.add_column(u'sfpirgapp_project', 'description_short',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Project.researcher_qualities'
        db.alter_column(u'sfpirgapp_project', 'researcher_qualities', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Project.description_long'
        db.alter_column(u'sfpirgapp_project', 'description_long', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Project.results_plan'
        db.alter_column(u'sfpirgapp_project', 'results_plan', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Project.time_per_week'
        db.alter_column(u'sfpirgapp_project', 'time_per_week', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Project.support_method'
        db.alter_column(u'sfpirgapp_project', 'support_method', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Project.larger_goal'
        db.alter_column(u'sfpirgapp_project', 'larger_goal', self.gf('django.db.models.fields.TextField')(null=True))
        # Deleting field 'Testimonial.author_email'
        db.delete_column(u'sfpirgapp_testimonial', 'author_email')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        u'sfpirgapp.actiongroup': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'ActionGroup'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'announcements': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'action_groups'", 'to': u"orm['sfpirgapp.Category']"}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'featured_image': ('sfpirgapp.fields.MyImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'goals': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'google_plus_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'group_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '(1, 2, 3, 4, 5)', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'links': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mailing_list_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meetings': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'oneliner': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'potential_members': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'theme_color': ('django.db.models.fields.CharField', [], {'default': "'grey'", 'max_length': '255'}),
            'timeline': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'twoliner': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actiongroups'", 'to': u"orm['auth.User']"})
        },
        u'sfpirgapp.actiongrouprequest': {
            'Meta': {'object_name': 'ActionGroupRequest'},
            'basis_of_unity': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'goals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_mailing_list': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'oneliner': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'potential_members': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'twoliner': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'sfpirgapp.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'sfpirgapp.application': {
            'Meta': {'object_name': 'Application'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sfpirgapp.Project']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        u'sfpirgapp.category': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Category'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'featured_image': ('sfpirgapp.fields.MyImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'theme_color': ('django.db.models.fields.CharField', [], {'default': "'grey'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categorys'", 'to': u"orm['auth.User']"})
        },
        u'sfpirgapp.dummytable': {
            'Meta': {'object_name': 'DummyTable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sfpirgapp.liaison': {
            'Meta': {'object_name': 'Liaison'},
            'alt_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'liaisons'", 'to': u"orm['sfpirgapp.Organization']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sfpirgapp.organization': {
            'Meta': {'object_name': 'Organization'},
            'communities': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'contact_alt_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_position': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mailing_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mailing_street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mailing_street2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mandate': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'sources_of_funding': ('mezzanine.core.fields.RichTextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'sfpirgapp.profile': {
            'Meta': {'object_name': 'Profile'},
            'bio': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on_mailing_list': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sfpirgapp.Organization']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'photo': ('sfpirgapp.fields.MyImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'sfpirgapp.project': {
            'Meta': {'object_name': 'Project'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'arx_projects'", 'to': u"orm['sfpirgapp.Category']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description_long': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '(1, 2, 3, 4, 5)', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_completed_successfully': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_underway': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'larger_goal': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'liaison': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sfpirgapp.Liaison']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'logo': ('sfpirgapp.fields.MyImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project_subject': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sfpirgapp.ProjectSubject']", 'symmetrical': 'False'}),
            'project_subject_other': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sfpirgapp.ProjectType']", 'symmetrical': 'False'}),
            'project_type_other': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'researcher_qualities': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'results_plan': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'support_method': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'time_per_week': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'sfpirgapp.projectsubject': {
            'Meta': {'object_name': 'ProjectSubject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'sfpirgapp.projecttype': {
            'Meta': {'object_name': 'ProjectType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'sfpirgapp.settings': {
            'Meta': {'object_name': 'Settings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sfpirgapp.testimonial': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Testimonial'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author_full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'testimonials'", 'to': u"orm['sfpirgapp.Category']"}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'featured_image': ('sfpirgapp.fields.MyImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'theme_color': ('django.db.models.fields.CharField', [], {'default': "'grey'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'testimonials'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['sfpirgapp']